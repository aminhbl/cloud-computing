import json
import os
import random
import string
from flask import Flask, request, redirect
from datetime import datetime
from mysql import connector as conn


def configs():
    try:
        with open('config.json', ) as file:
            return json.load(file)
    except FileNotFoundError or IOError:
        return {
            "server_port": 8080,
            "exp_time": 60,
            "database_host": "database",
            "database_password": "",
            "database_name": "database_name"
        }


conf = configs()

app = Flask(__name__)



def create_database_connection():
    if 'database_password' in os.environ:
        password = os.environ['database_password']
    else:
        password = conf['database_password']
    if 'database_name' in os.environ:
        name = os.environ['database_name']
    else:
        name = conf['database_name']
    try:

        c= conn.connect(user='root', host=conf['database_host'],
                        password=password,
                        database=name) 
        return c
    except Exception as e:
        print(str(e))
        return None


@app.route('/', methods=['POST'])
def create_short_url():

    data = request.get_data()
    if data:
        short_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        cur = None
        connection = None
        try:
            connection = create_database_connection()
            cur = connection.cursor()
            cur.execute("""INSERT INTO urls(short_url, long_url, start_time)
                        VALUES(%s, %s, %s)""", (short_url, data, datetime.utcnow()))
            connection.commit()
            return "urlshortener:{}/".format(conf['server_port']) + short_url
        except Exception as e:
            return "some thing went wrong: {}".format(str(e)), 500
        finally:
            if cur:
                cur.close()
            if connection:
                connection.close()
    else:
        return "enter a valid long url", 400


@app.route('/<short_url>', methods=['GET'])
def request_short_url(short_url):
    cur = None; 
    try:
	
        connection = create_database_connection(); 
        cur = connection.cursor()
        cur.execute("""SELECT long_url, start_time FROM urls WHERE short_url = %s""",
                    (short_url,))
        res = cur.fetchall(); 
	
        main_url, start_time = None, None
        if len(res) > 0:
            main_url, start_time = str(res[0][0]), res[0][1]

        if main_url:
            if (datetime.utcnow() - start_time).total_seconds() / 60 < conf['exp_time']:
                return redirect(main_url, code=302)
            else:
                cur.execute("""DELETE FROM urls WHERE short_url = %s""", (short_url,))
                connection.commit()
                raise Exception('enter valid short url')
        else:
            raise Exception('enter valid short url')
    except Exception as e:
        return f"some thing went wrong: {str(e)}", 400
    finally:
        if cur:
            cur.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=conf['server_port'])
