# Virtual Training Platform
>   Backend

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Usage
### Install & run locally
*   Create python3 virtualenv & activate it

    ```shell script
    python3 -m venv venv
    source venv/bin/activate
    ```
*   Install requirements

    ```shell script
    pip install -r requirements.txt 
    ```
*   Run `development` server
    ```shell script
    python main.py
    ``` 
    or for **hot-reloading..**
    ```shell script
    uvicorn main:application --reload
    ```