# Use an official Python runtime as a parent image
FROM python:3.12-slim

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Copy the current directory contents into the container at /api
ADD . /

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]