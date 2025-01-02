FROM python:3.12.0-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV APP=/app
WORKDIR $APP

COPY requirements.txt $APP/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . $APP/

WORKDIR $APP

EXPOSE 8000

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
