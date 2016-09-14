# coding: utf-8
import os, json, yaml, requests
from datetime import datetime
from flask import Flask, request
from OpenSSL import SSL

app = Flask(__name__)


class ChatBot(object):

    def __init__(self, debug=False):
        # fb messenger
        self.FACEBOOK_TOKEN = ''
        self.VERIFY_TOKEN = ''
        self.FBM_API = "https://graph.facebook.com/v2.6/me/messages"

        # flow ctrl
        self.debug = debug
        self.fbm_processed = []

        # load yaml setup
        with open("config.yaml", 'rt') as stream:
            try:
                cfg = yaml.load(stream)
                self.FACEBOOK_TOKEN = cfg.get('FACEBOOK_TOKEN')
                self.VERIFY_TOKEN = cfg.get('VERIFY_TOKEN')
            except yaml.YAMLError as exc:
                print(exc)


    def process_fbm(self, payload):
        for sender, msg in self.fbm_events(payload):
            self.fbm_api({"recipient": {"id": sender}, "sender_action": 'typing_on'})
            resp = self.gen_response(msg)
            self.fbm_api({"recipient": {"id": sender}, "message": {"text": resp}})
            if self.debug: print("%s: %s => resp: %s" % (sender, msg, resp))
            

    def gen_response(self, sent):
        #################################
        #   [MODIFY HERE !!!]
        #   you may add your own logic, 
        #   or even include your own language processing module from here!
        #################################
        sent = "MODIFY RESPONSE IN <gen_response>!!!"
        return sent



    #------------------------------
    #   FB Messenger API
    #------------------------------
    def fbm_events(self, payload):
        data = json.loads(payload.decode('utf8'))
        if self.debug: print("[fbm_payload]", data)
        for event in data["entry"][0]["messaging"]:
            if "message" in event and "text" in event["message"]:
                q = (event["sender"]["id"], event["message"]["seq"])
                if q in self.fbm_processed:
                    continue
                else:
                    self.fbm_processed.append(q)
                    yield event["sender"]["id"], event["message"]["text"]


    def fbm_api(self, data):
        r = requests.post(self.FBM_API,
            params={"access_token": self.FACEBOOK_TOKEN},
            data=json.dumps(data),
            headers={'Content-type': 'application/json'})
        if r.status_code != requests.codes.ok:
            print("fb error:", r.text)
        if self.debug: print("fbm_send", r.status_code, r.text)
        

#---------------------------
#   Server
#---------------------------
@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == self.VERIFY_TOKEN:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    bot.process_fbm(payload)
    return "ok"


#---------------------------
#   Start Server
#---------------------------
if __name__ == '__main__':
    bot = ChatBot(debug=True)
    # start server
    if True:
        context = ('ssl/server.crt', 'ssl/server.key')
        app.run(host='0.0.0.0', port=443, debug=False, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=80, debug=True)


