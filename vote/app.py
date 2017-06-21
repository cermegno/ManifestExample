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
	<a href="/survey">Choose dates for Pied Piper 2nd workshop</a><br>
	</h2>
	</BODY>
	"""
	return response

@app.route('/survey')
def survey():
    resp = make_response(render_template('survey.html'))
    return resp

@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():

    global r
##    c = request.form.getlist('cannot')
##    p = request.form['prefer']
##    print "Cannot do date is " + str(c)
##    print "Preferred date is " + p

    name = request.form['name']
    d1 = request.form['date1']
    d2 = request.form['date2']
    d3 = request.form['date3']
    d4 = request.form['date4']

    print "Name is " + name
    print "date 1 is " + d1
    print "date 2 is " + d2
    print "date 3 is " + d3
    print "date 4 is " + d4


    Counter = r.incr('ctr_vote2w')
    print "the counter is now: ", Counter
    ## Create a new key that includes the counter
    newvote = 'vote' + str(Counter)

    print "Storing vote : " + newvote
    ## Now the key name is the content of the variable newsurvey
    r.hmset(newvote,{'name':name,'d1':d1,'d2':d2,'d3':d3,'d4':d4})
	
    resp = """
    <h3> - THANKS FOR VOTING - </h3>
    """
    return resp

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
