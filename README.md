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

- rename `.env.sample` file on the parent directory to `.env`

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
NOTE - the heroku url for uploading file is currently down, i had an issue with my AWS account
    and heroku ephemeral system does not support cross worker paths. Please use the docker approach for now.
    ```
    https://song-counter.herokuapp.com/
    ```
- for the routes documentation
    ```
    https://song-counter.herokuapp.com/api/docs/
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

### Running the csv processor module as a standalone
You can also run the processor as a standalone by passing in file path on shell
- After cloning the repository navigate to the root folder
- create a new environment with `virtualenv venv`
- activate your environment `source venv/bin/activate`
- install requirements `pip install -r requirements.txt`

- run 
    ```
    venv/bin/python3 csv_filter_run.py <file/to/path.csv>
    ```
    Where file/to/path is replaced by the path to the actual csv file
- run our demo filter test with
    ``` venv/bin/python3 csv_filter_run.py test_csv.csv ```

- the processed file is stored in `media/processed/` folder

# How the entire flow works

## The Upload
Taking into consideration that the upload file might be larger than memory
Django MultiPartParser is used to break the files into smaller chunks, and stored in TemporaryNamedFile, which is then merged into one to reduce the strain on memory. 
- Why this is used?
The Parser is quite efficient and is one of the most straightforward way to  handle large files. To really scale up the efficiency, we will have to use a third party file hoster.

### The CSV Processing
To provide the most efficient threading performance to work on a large csv file larger than memory, dask was used

### How Dask works
Dask can efficiently perform parallel computations on a single machine using multi-core CPUs. For example, if you have a quad core processor, Dask can effectively use all 4 cores of your system simultaneously for processing. In order to use lesser memory during computations, Dask stores the complete data on the disk, and uses chunks of data (smaller parts, rather than the whole data) from the disk for processing. During the processing, the intermediate values generated (if any) are discarded as soon as possible, to save the memory consumption.

In summary, Dask can run on a cluster of machines to process data efficiently as it uses all the cores of the connected machines. One interesting fact here is that it is not necessary that all machines should have the same number of cores. If one system has 2 cores while the other has 4 cores, Dask can handle these variations internally.

### Space and Time Complexity
The Time complexity for the processing is O(NLogN)
The Space Complexity is O(N)