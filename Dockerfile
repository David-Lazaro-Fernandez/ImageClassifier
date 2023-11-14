# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .h5 file into the container at /app
COPY model.h5 /app/

# Copy the rest of the current directory contents into the container at /app
COPY . /app

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Define the command to run your FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
