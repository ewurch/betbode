# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages for Firefox and GeckoDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    firefox-esr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install GeckoDriver
RUN GECKO_DRIVER_VERSION=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4) && \
    wget -q --continue -P /tmp "https://github.com/mozilla/geckodriver/releases/download/${GECKO_DRIVER_VERSION}/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin/ && \
    rm /tmp/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz

# Set display port to avoid crash
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy requirements.txt to working directory
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run the web scraping script
CMD ["python", "main.py"]
