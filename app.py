#!/usr/bin/env python

import urllib
import json
import os
import urllib.request
    
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

    freeboxIp = '82.66.190.153:8081';
    freeboxCodeTel = '21357594';
    url = 'http://' + freeboxIp + '/pub/remote_control?code=' + freeboxCodeTel + '&key=';
    
        
def makeWebhookResult(req):
    if req.get("result").get("action") != "freebox.chaines":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("Chaines")
        action = parameters.get("freebox.action")

        cost = {'1':'TF1', '2':'france 2', '3':'france 3', '4':'canal plus', '5':'france 5', '6':'M 6'}
        speech = cost[zone] + " va être lancé sur votre Freebox."

        url = url + zone;
        page = urllib.request.urlopen(url) 
        strpage = page.read()
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-freebox"
        }
    elif req.get("result").get("action") != "freebox.actions":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("Chaines")

        cost = {'1':'power', '2':'tv', '3':'power', '4':'power', '5':'power', '6':'power'}
        speech = cost[zone] + " va être lancé sur votre Freebox."

        url = url + zone;
        page = urllib.request.urlopen(url) 
        strpage = page.read()
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-freebox"
        }
    
    else:
        return {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
