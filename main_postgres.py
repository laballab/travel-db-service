# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_psql]
import os


from flask import Flask
from flask import request 
import psycopg2
import json

#db_user = os.environ.get('CLOUD_SQL_USERNAME')
#db_password = os.environ.get('CLOUD_SQL_PASSWORD')
#db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
#db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

import users
import trips
import transactions

#users_db_cols = ('user_id','username','password','firstname','lastname')

db_user = 'dbadmin'
db_password = 'admin1!'
db_name = 'postgres'
db_connection_name = 'skilful-courage-220001:us-east1:travel-db-instance'

app = Flask(__name__)
app.register_blueprint(users.mod)
app.register_blueprint(trips.mod)
app.register_blueprint(transactions.mod)


@app.route('/')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV'):
        # If deployed, use the local socket interface for accessing Cloud SQL
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'

    cnx = psycopg2.connect(dbname=db_name, user=db_user,
                           password=db_password, host=host)

    result = []
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM users;')
        for row in cursor.fetchall():
          result.append(dict(zip(users_db_cols,row)))

    cnx.commit()
    cnx.close()

    return str(json.dumps(result))
# [END gae_python37_cloudsql_psql]

'''
@app.route('/user/<user_id>', methods=['GET'])
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

@app.route('/create/user', methods=['GET'])
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
'''

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
