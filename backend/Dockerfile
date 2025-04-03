# Use the official Python 3.9 image from Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# # Install ffmpeg and other necessary packages
# RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the source code into the container
COPY ./src /code/src

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "src.main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]
