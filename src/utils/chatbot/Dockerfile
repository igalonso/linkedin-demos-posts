# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements-chatbot.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application when the container launches
CMD ["python", "chat_bot_backend.py"]