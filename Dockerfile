# Use the official Python image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    git \
    libgl1-mesa-glx

RUN pip install protobuf==3.20.2

# Clone ByteTrack repository
RUN git clone https://github.com/ifzhang/ByteTrack.git
WORKDIR /app/ByteTrack

# Install Python dependencies
# RUN pip install numpy
RUN pip install numpy==1.23.5
RUN pip install -r requirements.txt

# Setup ByteTrack
RUN python3 setup.py develop

# Install additional dependencies
RUN pip install cython
RUN pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
RUN pip install cython_bbox

# Move back to the working directory
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

# Expose the port Flask is running on
EXPOSE 5000

# Copy the current directory contents into the container at /app
COPY . .

# Command to run the Flask application
# CMD [ "python", "main.py" ]

CMD exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 8 --timeout 0 run:app
