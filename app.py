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

# http://90.73.151.42:8085/remoteControl/cmd?operation=10
    liveboxIp = '90.73.151.42:8085';
    url = 'http://' + liveboxIp + '/remoteControl/cmd?operation=';
    url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key=116&mode=0';

def makeWebhookResult(req):
    if req.get("result").get("action") != "livebox.Chaines":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("ListeDesChaines")
        action = parameters.get("livebox.Chaines")

        cost = {'1':'TF1', '2':'france 2', '3':'france 3', '4':'canal plus', '5':'france 5', '6':'M 6'}
        # speech = cost[zone] + " va être lancé sur votre livebox."
        speech = zone + " va être lancé sur votre livebox."

        url = url;
        page = urllib.request.urlopen(url2) 
        strpage = page.read()
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-livebox"
        }
    elif req.get("result").get("action") != "livebox.Actions":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("ListeDesChaines")

        cost = {'1':'power', '2':'tv', '3':'power', '4':'power', '5':'power', '6':'power'}
        speech = cost[zone] + " l action à été lancé."

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
            "source": "apiai-worganic-livebox"
        }
    
    else:
        return {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print("Starting aa app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
