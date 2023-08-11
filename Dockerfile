# Build Stage
FROM python as build

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Runtime Stage
FROM python:alpine as runtime

WORKDIR /app

# Copy only necessary files from the build stage
COPY --from=build /app /app

# Runtime dependencies
RUN pip install --no-cache-dir uvicorn fastapi pycountry 

# Copy python-native packages from build stage to runtime stage
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# Set the entrypoint command
CMD ["uvicorn", "main:app", "--port", "8000"]
