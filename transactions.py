import os
import datetime 

#import main_postgres

#from main_postgres import app

from flask import Flask, request, Blueprint
import psycopg2
import simplejson as json

mod = Blueprint('transactions',__name__)

transactions_db_cols = ('transaction_id','trip_id','user_id','description', 'amount', 'personal')

db_user = 'dbadmin'
db_password = 'admin1!'
db_name = 'postgres'
db_connection_name = 'skilful-courage-220001:us-east1:travel-db-instance'


@mod.route('/transaction', methods=['GET'])
def getTransaction():
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    trip_id = request.args.get('tripID', '')
    user_id = request.args.get('userID', '')

    result = []
    with cnx.cursor() as cursor:
        if user_id == '':
            query = ('SELECT transaction_id, trip_id, user_id, description, amount, personal FROM transactions WHERE trip_id='
                      +trip_id+ ';')
        elif trip_id == '':
            query = ('SELECT transaction_id, trip_id, user_id, description, amount, personal FROM transactions WHERE user_id='
                      +user_id+ ';')
        else:
            query = ('SELECT transaction_id, trip_id, user_id, description, amount, personal FROM transactions WHERE trip_id='
                      +trip_id+ ' AND user_id='
                      +user_id+ ';')

        cursor.execute(query)
        for row in cursor.fetchall():
          result.append(dict(zip(transactions_db_cols,row)))

    cnx.commit()
    cnx.close()

    return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]

@mod.route('/create/transaction', methods=['GET'])
def createTransaction():
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)
    
    trip_id = request.args.get('tripID', '')
    user_id = request.args.get('userID', '')
    description = request.args.get('description', '')
    amount = request.args.get('amount', '')
    dateTime = str(datetime.datetime.now())
    if(request.args.get('personal', '') == 'true'): personal = str(True)
    else: personal = str(False)

    #result = []
    with cnx.cursor() as cursor:
        cursor.execute("INSERT INTO transactions (trip_id, user_id, description, amount, datetime, personal) VALUES ('" +trip_id+ "','" +user_id+ "','" +description+ "','" +amount+ "','" +dateTime+ "','" +personal+ "');")
        #for row in cursor.fetchall():
          #result.append(dict(zip(transactions_db_cols,row)))

    cnx.commit()
    cnx.close()
    return ('SUCCESS')

    #return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]
