import os

#import main_postgres

#from main_postgres import app

#from flask import Flask, request, Blueprint
from flask import request, Blueprint
import psycopg2
import simplejson as json

mod = Blueprint('trips',__name__)

trips_db_cols = ('trip_id','user_id','amount_due','trip_name')

db_user = 'dbadmin'
db_password = 'admin1!'
db_name = 'postgres'
db_connection_name = 'skilful-courage-220001:us-east1:travel-db-instance'


@mod.route('/trip', methods=['GET'])
def getTrip():
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    user_id = request.args.get('userID', '')
    trip_name = request.args.get('tripName', '')
    
    result = []
    with cnx.cursor() as cursor:
        if user_id == '':
            query = ('SELECT * FROM trips WHERE trip_name='
                      +trip_name+ ';')
        elif trip_name == '':
            query = ('SELECT * FROM trips WHERE user_id='
                      +user_id+ ';')
        else:
            query = ('SELECT * FROM trips WHERE trip_name='
                      +trip_name+ ' AND user_id='
                      +user_id+ ';')

        cursor.execute(query)
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
    
    user_id = request.args.get('userID', '')
    amount_due = request.args.get('amountDue', '')
    trip_name = request.args.get('tripName', '')

    #result = []
    with cnx.cursor() as cursor:
        cursor.execute("INSERT INTO trips (user_id, amount_due, trip_name) VALUES ('" +user_id+ "','" +amount_due+ "','" +trip_name+ "');")
        #for row in cursor.fetchall():
          #result.append(dict(zip(trips_db_cols,row)))

    cnx.commit()
    cnx.close()

    result = dict([('tripName',trip_name)])
    return str(json.dumps(result))

    #return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]
