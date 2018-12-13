# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory to /DockerPolyHash
WORKDIR ./DockerPolyHash

# Copy the current directory contents into the container at /DockerPolyHash
COPY . /DockerPolyHash

# Install any needed packages specified in Pipfile.lock
RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# Run DockerPolyHash.py when the container launches
RUN pipenv run python3 ./src/main.py