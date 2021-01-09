from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import webbrowser
import db

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""
start_date = time.ctime()
start_day_number = start_date.split()[2]
start = True
inital = None
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
    global start
    current_date = time.ctime()
    current_day_number = current_date.split()[2]
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    parent_url = url_strip(url)
    print("currently viewing: " + parent_url)

    global url_timestamp
    global url_viewtime
    global prev_url

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0
    else:
        if url_viewtime[parent_url] >= 2000:
            webbrowser.open('https://psugroupfind.herokuapp.com/')
    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent
    
    if int(current_day_number) < int(start_day_number):
        for key in url_viewtime:
            url_viewtime[key] = 0
        start = True
        
    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    print("final vietimes: ", url_viewtime)
    all_data = {"date" : current_date, "Websites":url_viewtime}
    global initial
    if start:
        initial = db.user_collection.insert_one(all_data)
        initial = initial.inserted_id
        start = False
    else:
        db.user_collection.find_and_modify({"date",""})
    
    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=["POST"])
def quit_url():
    resp_json = request.get_data()
    print("URL closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

@app.route('/home', methods=["GET"])
def home():
    global url_viewtime
    return jsonify({
        url_viewtime})



app.run(threaded=True, port=5000)