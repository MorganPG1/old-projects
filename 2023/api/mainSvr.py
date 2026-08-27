
from random import randrange
from flask import Flask, request
app = Flask(__name__)
@app.route('/', methods=['Get'])
def result():
    print(request.args.get('max'))
    b = int(request.args.get('max'))
    a = randrange(1,b)
    print("Responded with " + str(a))
    
    return '<h1<p style="text-align: center;">Test Python Server</span></p><p style="text-align: center;"></p><p style="text-align: left;">Random Number: '+str(a)+'</p><p style="text-align: left;">Range: 1-'+str(b)+'</p><p style="text-align: left;"></p><p style="text-align: center;">To generate a random number change the max value in the URL</p>'
    
app.run(host="192.168.1.184", port=2556)