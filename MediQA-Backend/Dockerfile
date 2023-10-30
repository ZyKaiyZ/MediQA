# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Node.js and npm using apt-get
RUN apt-get update && apt-get install -y nodejs npm

# Install any needed packages specified in requirements.txt
RUN apt-get install -y git
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run your Python script
CMD ["python", "main.py"]
