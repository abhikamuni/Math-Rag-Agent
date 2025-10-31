
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the backend application code
COPY ./app /code/app
COPY ./scripts /code/scripts
COPY ./optimized_refiner_module.json /code/optimized_refiner_module.json

# Expose port 7860 (Hugging Face's default)
EXPOSE 7860

# Run uvicorn. Note: We use 7860, not $PORT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
