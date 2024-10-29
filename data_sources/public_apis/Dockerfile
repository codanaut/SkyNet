# Build With:
# docker buildx build -f .\Dockerfile.master --platform=linux/arm64 --push -t registry.gitlab.com/codanaut/projects/logger:master .

# Run with:
# docker run --name flight-logger-master -d registry.gitlab.com/codanaut/projects/logger:master

# Use an official Python runtime as the base image
FROM python:3.12

# Set the timezone in a slightly different way to avoid potential issues
ENV TZ=America/Denver
RUN apt-get update && apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
ENV PYTHONUNBUFFERED=1


# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the container
COPY . .

# Specify the command to run your Flask app within the container
CMD ["python", "aircraft_api_logger.py"]
