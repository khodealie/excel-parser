# Use an official lightweight Python image as a parent image
FROM python:3.10-slim

# Set environment variables to minimize Python bytecode generation and buffer logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install the requirements
COPY ./req.txt /app/req.txt
RUN pip install --upgrade pip \
    && pip install -r req.txt

# Copy the project files into the container
COPY . /app
