# Use the official alpine image as base image
FROM python:alpine

# Set the working directory within the container
WORKDIR /main

# Install pip first
# NOTE: Alpine uses apk for package manager, while apt exists for Linux
# NOTE: build-base(gcc) resolves the issue of buildling wheel for mysqlclient
RUN apk add --no-cache python3 py3-pip mariadb-dev build-base mariadb-connector-c-dev pkgconf
RUN pip3 install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies with headers for MySQL
RUN pip3 install --no-cache-dir mysqlclient==2.2.0

# Install the required dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of app code into container
COPY . .

# Expose port 5000 to the host
EXPOSE 5000

# Define the command to run the application
# NOTE: app will continue running as a web server
CMD ["python", "main.py", "--foreground"]