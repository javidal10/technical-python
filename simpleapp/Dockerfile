# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install PostgreSQL client dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the working directory
COPY . /code/

# Set environment variables
ENV DB_NAME IsiTechnicalbackend
ENV DB_USER IsiTechnical
ENV DB_PASSWORD 12345678Isi
ENV DB_HOST postgres
ENV DB_PORT 5432
ENV DB_SECRET_KEY django-insecure-vx(8sf1fr&_)=d-4hnud44vata*=rbv_v)duirwhkmsc8=$g0+

# Expose the port on which your Django app will run (change it to the appropriate port)
EXPOSE 8000

# Run database migrations and the development server
CMD python manage.py migrate && python manage.py runserver