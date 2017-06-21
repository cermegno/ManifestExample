import os
import redis
import json
from flask import Flask, render_template, redirect, request, url_for, make_response

if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
else:
    r = redis.Redis(host='127.0.0.1', port='6379')

app = Flask(__name__)

@app.route('/')
def mainpage():

	response = """
	<HTML><BODY><h2>
	<a href="/dumpvotes">Dump votes for Pied Piper 2nd workshop</a><br>
	</h2>
	</BODY>
	"""
	return response

@app.route('/dumpvotes')
def dumpvotes():

    global r
    response = "Dump of all votes so far<br>"
    response += "-----------------------<br>"
    response += "Name,13 July, 20 July, 27 July, 3 Aug<br>"
    print "Reading back from Redis"
    for v in r.keys('vote*'):
        print v
        response += r.hget(v,'name') + ","
        response += r.hget(v,'d1') + "," + r.hget(v,'d2') + ","
        response += r.hget(v,'d3') + "," + r.hget(v,'d4') + "<br>"
    response += " ----------------------<br>"

    return response

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5001')), threaded=True)
