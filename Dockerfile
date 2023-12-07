# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the Docker container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./src /code/src

# Copy other necessary files like alembic.ini and .env to the working directory
COPY alembic.ini .env ./

# Specify the command to run on container start
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

# Expose the port the app runs on
EXPOSE 8080
