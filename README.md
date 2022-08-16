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
