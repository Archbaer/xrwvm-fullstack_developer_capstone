from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments
import logging
import json

logger = logging.getLogger(__name__)


def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    else:
        response_data = {"userName": username, "status": "Authentication Failed"}

    return JsonResponse(response_data)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail['review']).get('sentiment')
            review_detail['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            # response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})
