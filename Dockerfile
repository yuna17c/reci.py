# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        gcc \
        postgresql \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /app/

# Expose the port that Django runs on
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]