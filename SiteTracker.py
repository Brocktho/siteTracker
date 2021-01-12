from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import webbrowser
from db import user_collection
import os
from dataStructures import Node, Queue

app = Flask(__name__)
secret = os.urandom(16)
url_timestamp = {}
url_viewtime = {}
prev_url = ""
start_date = time.ctime()
start_day_number = start_date.split()[2]
start = True
inital = None
hold = None
q = Queue()
CORS(app)


def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", "").replace("http://", "").replace('\"', "")
    if "/" in url:
        url = url.split("/", 1)[0]
    if "." in url:
        url = url.replace(".","_")
    return url

@app.route('/send_url', methods=['POST'])
def send_url():
    global q
    global url_timestamp
    global url_viewtime
    global prev_url
    global initial
    global start
    global hold
    current_date = time.ctime()
    current_day_number = current_date.split()[2]
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    parent_url = url_strip(url)
    first = Node('print("currently viewing: " + parent_url)')
    q.enqueue(first)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent
    
    if int(current_day_number) > int(start_day_number):
        for key in url_viewtime:
            url_viewtime[key] = 0
        start = True
        
    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    second = Node('print("final timestamps: ", url_timestamp)')
    q.enqueue(second)
    third = Node('print("final viewtimes: ", url_viewtime)')
    q.enqueue(third)
    all_data = {"date" : current_date, "Websites":url_viewtime}
    if start:
        fourth = Node('user_collection.insert_one(all_data)')
        q.enqueue(fourth)
        fifth = Node('hold.inserted_id')
        q.enqueue(fifth)
        start = False
    else:
        fourth = Node('user_collection.update({"_id": initial}, {"date": current_date, "Websites":url_viewtime})')
        q.enqueue(fourth)
    while len(q) != 0:
        current = exec(q.dequeue())
        if current == hold.inserted_id:
            initial = current
        hold = current

        
    
    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=["POST"])
def quit_url():
    resp_json = request.get_data()
    print("URL closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

@app.route('/home', methods=["GET"])
def home():
    global url_viewtime
    return jsonify({'message':
        url_viewtime})
