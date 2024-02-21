#FROM python:3.11-alpine

#WORKDIR /app

#COPY . /app

#RUN pip3 install -r requirements.txt

#ENV FLASK_APP=./server.py

#CMD ["flask", "run", "--host=0.0.0.0"]
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=server.py

# Run flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
