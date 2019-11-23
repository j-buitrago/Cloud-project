import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('db',27017)
#client.drop_database('twitterdb')
db = client.twitterdb

@app.route('/')
def todo():

    _items = db.twitterdb.find()
    items = [item for item in _items]

    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)