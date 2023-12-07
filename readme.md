To run the backend for the application you must first create the .env file
The .env file details should've been given to you, create a .env file in the root directory


## Execute the following commands

docker build -t myfastapiapp .
docker run -p 8080:8080 myfastapiapp