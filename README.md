# csv_parser
Built to specifically process/parse csv files, looking at duplicated songs in particular dates and getting the total counts of those songs

## Technology Stack

- Django
- DRF(Django Rest Framework)
- Celery
- Redis
- Dask
- Pandas

###  Setting Up For Local Development
- clone the repository 
    ```
    git clone https://github.com/ferrumie/csv-parser.git
    ```
- navigate to the parent folder

- Ensure you have docker installed

- Go through the official docker docs for a quick guide on how to install docker

- https://docs.docker.com/engine/install/ubuntu/

- run 
    ```
    docker-compose up --build
    ```
- This will automatically run the app in a container and route it to the local server

- for the route documentation
    ```
    http://127.0.0.1:8000/api/docs/
    ```

###  Setting up heroku
- using postman or any other API platform
- send requests to the app link
    ```
    https://song-counter.herokuapp.com/
    ```
- for the routes documentation
    ```
    https://song-counter.herokuapp.com/
    ```

### Uploading CSV Files
To upload a CSV File, we will be sending a POST request to the /api/upload/ route
- Open up your postman or any other API platform
- In the request url pane, input the upload route
    ```
    https://song-counter.herokuapp.com/api/upload 
    ``` for deployed url
    ```
    http://127.0.0.1:8000/api/upload/
    ``` for docker user
- in the header, ensure Content-Type is set to 
    ```
    multipart/form-data;
    ```
- upload your file with the "file" key under request body form-data
- click on send
- This should automatically process the file in the background and return a `processing_id`

### Retriving Uploaded File
After the upload is completed, a task in run in the background to filter out and process the csv file. and after this is complete, you can view your processed data. This is a GET request
- In the request url pane, input the retrieve route with a GET request
    ```
    https://song-counter.herokuapp.com/api/file/<processing_id>/ 
    ``` processing id is the id gotten after you uploaded the csv file
    ```
    http://127.0.0.1:8000/api/file/<processing_id>/
    ``` for docker user
- if the file is ready you will see the link to the file processed, if it is not you will see a message telling that it is not ready
- click on the file link to download the processed file