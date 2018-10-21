import os

#import main_postgres

#from main_postgres import app

from flask import Flask, request, Blueprint
import psycopg2
import json

mod = Blueprint('trips',__name__)

trips_db_cols = ('trip_id','user_id','amount_due','trip_name')

db_user = 'dbadmin'
db_password = 'admin1!'
db_name = 'postgres'
db_connection_name = 'skilful-courage-220001:us-east1:travel-db-instance'


@mod.route('/trip/<trip_id>', methods=['GET'])
def getTrip(trip_id):
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    result = []
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM trips WHERE trip_id='
                      +trip_id+ ';')
        for row in cursor.fetchall():
          result.append(dict(zip(trips_db_cols,row)))

    cnx.commit()
    cnx.close()

    return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]

@mod.route('/create/trip', methods=['GET'])
def createTrip():
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)
    
    user_id = request.args.get('user_id', '')
    amount_due = request.args.get('amountDue', '')
    trip_name = request.args.get('tripName', '')

    #result = []
    with cnx.cursor() as cursor:
        cursor.execute("INSERT INTO trips (user_id, amount_due, trip_name) VALUES ('" +user_id+ "','" +amount_due+ "','" +trip_name+ "');")
        #for row in cursor.fetchall():
          #result.append(dict(zip(trips_db_cols,row)))

    cnx.commit()
    cnx.close()
    return ('SUCCESS')

    #return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]
