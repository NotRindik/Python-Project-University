# Use the official Python 3.13 runtime image as the base image
FROM python:3.13

# Create and set the working directory inside the container
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy requirements.txt into the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose port 8000 so the Django app is accessible
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]