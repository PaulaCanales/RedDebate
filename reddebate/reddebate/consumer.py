from channels import Group
import threading
import random

def sendmsg(num):
    Group('stocks').send({'text':num})

t = 0
count = 0
def periodic(sms):
    global t;
    # n = random.randint(10,200);
    # sendmsg(str(n))
    Group('stocks').send({'text':sms})
    t = threading.Timer(5, periodic)
    t.start()

def ws_message(message):
    global t
    print(message.content['text'])
    if ( message.content['text'] != 'stop'):
        periodic(message.content['text'])
    else:
        t.cancel()

def ws_connect(message):
    Group('stocks').add(message.reply_channel)
    Group('stocks').send({'text':'connected'})


def ws_disconnect(message):
    Group('stocks').send({'text':'disconnected'})
    Group('stocks').discard(message.reply_channel)
