# Use an official Python 3.11 runtime as an image
FROM python:3.12.4-alpine3.19

# Create non-privileged user
RUN useradd -m -s /bin/bash appuser

# Set working directory in the container
WORKDIR /app

# Install modules while staging
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Change ownership of application files to non-privileged user
RUN chown -R appuser:appuser /app
USER appuser
RUN whoami

# Don't forget to cover this with IPTables or server firewall
EXPOSE 8000

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]