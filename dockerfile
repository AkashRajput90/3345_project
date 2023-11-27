# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 80


# Define environment variables for MongoDB connection
ENV MONGO_URI mongodb://mongo:27017/blog_db

# Install MongoDB in the container (if not using an external instance)
#RUN apt-get update && apt-get install -y mongodb

# Run app.py when the container launches
CMD ["python", "app.py"]