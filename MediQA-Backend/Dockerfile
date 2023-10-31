# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Node.js and npm using apt-get
RUN apt-get update
RUN apt-get install curl gnupg -y
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install nodejs -y

# Install any needed packages specified in requirements.txt
RUN apt-get install -y git
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run your Python script
CMD ["python", "main.py"]
