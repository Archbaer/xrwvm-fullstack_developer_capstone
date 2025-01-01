from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def get_car_makes(request):
    car_makes = CarMake.objects.all()
    car_make_data = []
    for car_make in car_makes:
        car_make_data.append({
            'name': car_make.name,
            'description': car_make.description
        })
    return JsonResponse({'car_makes': car_make_data})


@csrf_exempt
def get_car_models(request, car_make_id):
    try:
        car_make = CarMake.objects.get(id=car_make_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Car make not found'}, status=404)

    car_models = CarModel.objects.filter(car_make=car_make)
    car_model_data = []
    for car_model in car_models:
        car_model_data.append({
            'name': car_model.name,
            'type': car_model.type,
            'year': car_model.year
        })
    return JsonResponse({'car_models': car_model_data})


@csrf_exempt
def add_car_make(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        car_make = CarMake.objects.create(name=name, description=description)
        return JsonResponse({'message': f'{car_make.name} added successfully'})


@csrf_exempt
def add_car_model(request):
    if request.method == 'POST':
        car_make_id = request.POST.get('car_make_id')
        name = request.POST.get('name')
        type = request.POST.get('type')
        year = request.POST.get('year')

        try:
            car_make = CarMake.objects.get(id=car_make_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Car make not found'}, status=404)

        car_model = CarModel.objects.create(
            car_make=car_make, name=name, type=type, year=year
        )
        return JsonResponse({'message': f'{car_model.name} added successfully'})


@csrf_exempt
def update_car_model(request, car_model_id):
    if request.method == 'PUT':
        try:
            car_model = CarModel.objects.get(id=car_model_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Car model not found'}, status=404)

        name = request.PUT.get('name')
        type = request.PUT.get('type')
        year = request.PUT.get('year')

        car_model.name = name if name else car_model.name
        car_model.type = type if type else car_model.type
        car_model.year = year if year else car_model.year
        car_model.save()

        return JsonResponse({'message': 'Car model updated successfully'})
