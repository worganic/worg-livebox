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
    # url = 'http://' + liveboxIp + '/remoteControl/cmd?operation=';
    url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key=116&mode=0';

def makeWebhookResult(req):
    if req.get("result").get("action") != "livebox.Chaines":
        liveboxIp = '90.73.151.42:8085'
        url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key=116&mode=0'
        url2 = 'http://' + liveboxIp + '/remoteControl/cmd?operation=01&key='
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("ListeDesChaines")
        #zone1 = str(zone)
        print(zone)
        zone1 = zone[0]
        print(zone1)

        
        cost = {'c1':'TF1', 'c2':'France 2', 'c3':'France 3', 'c4':'Canal plus', 'c5':'France 5', 'c6':'M 6'}
        print(cost[zone1])
        speech = "La chaîne " + str(cost[zone1]) + " va être lancé."
        
        zone1 = zone1.replace("c", "")
        zone2 = int(zone1)

        code = {'0':'512', '1':'513', '2':'514', '3':'515', '4':'516', '5':'517', 6:'518', '7':'519', '8':'520', '9':'521'}

        unite = zone2 % 10
        dizaine = (zone2 % 100) / 10
        centaine = (zone2 % 1000) / 100
        print(centaine)
        print(dizaine)
        print(unite)
        
        if centaine > 0.9:
            codeA = code[centaine]
            url = url2 + codeA + '&mode=0'
            page = urllib.request.urlopen(url) 
            #strpage = page.read()
            print(url)

        if dizaine > 0.9:
            codeA = code[dizaine]
            url = url2 + codeA + '&mode=0'
            page = urllib.request.urlopen(url) 
            #strpage = page.read()
            print(url)

        codeA = code[unite]
        print(codeA)
        url = url2 + codeA + '&mode=0'
        page = urllib.request.urlopen(url) 
        #strpage = page.read()
        print(url)
        
        print("Response:")
        print(speech)

        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            # "contextOut": [],
            "source": "apiai-worganic-livebox",
            "urlA": url 
        }
    elif req.get("result").get("action") != "livebox.Actions":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("actionPlus")
        action = parameters.get("livebox.Actions")

        cost = {'1':'power', '2':'tv', '3':'power', '4':'power', '5':'power', '6':'power'}
        speech = cost[zone] + " l action à été lancé."

        # url = url + zone;
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
    
    else:
        return {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print("Starting aa app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
