import os

#import main_postgres

#from main_postgres import app

from flask import Flask, request, Blueprint
import psycopg2
import json

mod = Blueprint('users',__name__)

users_db_cols = ('user_id','username','password','firstname','lastname')

db_user = 'dbadmin'
db_password = 'admin1!'
db_name = 'postgres'
db_connection_name = 'skilful-courage-220001:us-east1:travel-db-instance'


@mod.route('/user/<user_id>', methods=['GET'])
def getUser(user_id):
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    result = []
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE user_id='
                      +user_id+ ';')
        for row in cursor.fetchall():
          result.append(dict(zip(users_db_cols,row)))

    cnx.commit()
    cnx.close()

    return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]

@mod.route('/create/user', methods=['GET'])
def createUser():
    if os.environ.get('GAE_ENV'):
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    username = request.args.get('username', '')
    password = request.args.get('password', '')
    firstname = request.args.get('firstname', '')
    lastname = request.args.get('lastname', '')

    #result = []
    with cnx.cursor() as cursor:
        cursor.execute("INSERT INTO users (username,password,firstname,lastname) VALUES ('" +username+ "','" +password+ "','" +firstname+ "','" +lastname+ "');")
        #for row in cursor.fetchall():
          #result.append(dict(zip(users_db_cols,row)))

    cnx.commit()
    cnx.close()
    return ('SUCCESS')

    #return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]
