from flask import Flask
from flask import render_template
import MySQLdb
import logging
import os
import json, simplejson
import tornado.options
import urllib
from django.utils.encoding import smart_str
from tornado.options import define, options

define("mysql_hostname")
define("mysql_user")
define("mysql_password")
define("mysql_database")
define("textProcessingUrl")


path = os.path.join(os.path.dirname(__file__), "settings.py")
tornado.options.parse_config_file(path)

conn = MySQLdb.connect(options.mysql_hostname, options.mysql_user, options.mysql_password, options.mysql_database, charset = "utf8", use_unicode = True)
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

app = Flask(__name__)
app.debug = True

@app.route("/")
def Welcome():
    return "Landing page of Twitter Sentiments!"

@app.route("/query/<query>/<int:last_id>/<int:max_result>/<return_format>")
@app.route("/query/<query>/<int:last_id>/<return_format>")
@app.route("/query/<query>/<return_format>")
@app.route("/query/<query>")
@app.route("/query/<query>/")
def query(query, last_id=0, max_result=10, return_format=''):
    query = urllib.quote(query)
    if last_id == 0:
        db_query = "SELECT * FROM sentiments where query = '%s' ORDER BY id DESC limit %d" % (query, max_result);
    else:
        db_query = "SELECT * FROM sentiments where query = '%s' AND id < %d ORDER BY id DESC limit %d" % (query, last_id, max_result);
    print db_query
    try:
        cursor.execute(db_query)
        tweets = []
        for n in range(cursor.rowcount):
            row = cursor.fetchone()
            tweets.append(row)
        if return_format == 'json':
            return simplejson.dumps(tweets)
        elif return_format == 'append':
            return render_template("append_sentiments.html", count = cursor.rowcount, query=query, tweets=tweets )
        else:
            return render_template("show_sentiments.html", count = cursor.rowcount, query=query, tweets=tweets )
    except:
        return "Error while inserting into database" + db_query

if __name__ == "__main__":
    app.run()
