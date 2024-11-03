# Use a base image with Python and pytest pre-installed
FROM python:3.9-slim

# Set the working directory in the Docker image
WORKDIR /app

# Copy the application code and test files into the image
COPY . /app

# Install any additional dependencies required by your application or tests
RUN pip install -r requirements.txt

# Run pytest with the -v flag when the Docker container starts
CMD ["pytest", "-v"]
