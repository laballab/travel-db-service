image:: https://img.shields.io/badge/python-3.6.5-brightgreen.svg

# travel-db-service
Flask database webservice used as part of a project for HackGT 2018! 

## Installation
pip install -r requirements.txt

## Proxy
./cloud_sql_proxy -instances=skilful-courage-220001:us-east1-b:travel-db-instance=tcp:5432 -credential_file skilful-courage-220001-4518022460f3.json 

## Running
source env/postgres/bin/activate
