# Use the official Python slim image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Update package sources and install netcat
RUN apt-get update \
    && apt-get install -y netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Set the application directory
ENV APP=/app
WORKDIR $APP

# Copy the requirements file and install dependencies
COPY requirements.txt $APP
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . $APP

# Expose the application port
EXPOSE 8000

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]

# Default command to start the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
