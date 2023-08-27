# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the 'flask' directory into the container at /app/flask
COPY ./flask /app/flask/

# Change the working directory to the flask directory
WORKDIR /app/flask

# Specify the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Open port 5000 for the Flask app to listen on
EXPOSE 5000

# Define the command to run the Flask app
CMD ["flask", "run"]
