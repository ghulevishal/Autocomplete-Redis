#redis client ofr python
import redis
#flask to expose api's to outside world
from flask import Flask,request,jsonify
app = Flask("autocomplete")

#creating a redis connection
r = redis.StrictRedis(host='localhost', port=7001, db=0)

#route to add a value to autocomplete list
'''
FORMAT:
localhost:5000/add?name=<name>
'''
@app.route('/add')
def add_to_dict():
    try:
        name = request.args.get('name')
        n = name.strip()         
        for l in range(1,len(n)):             
            prefix = n[0:l]             
            r.zadd('compl',{prefix:0})
        r.zadd('compl',{n+"*":0})
        return "Added"
    except:
        return "Addition failed"


#route to get the suggestiosn
'''
FORMAT:
localhost:5000/suggestions?prefix=<prefix_you want to match>
'''
@app.route('/suggestions')
def get_suggestions():
    prefix = request.args.get('prefix')
    results = []
    rangelen = 50 # This is not random, try to get replies < MTU size
    count=5
    start = r.zrank('compl',prefix)    
    if not start:
        return []
    while (len(results) != count):         
         range = r.zrange('compl',start,start+rangelen-1)         
         start += rangelen
         if not range or len(range) == 0:
             break
         for entry in range:
             entry=entry.decode('utf-8')
             minlen = min(len(entry),len(prefix))   
             if entry[0:minlen] != prefix[0:minlen]:    
                count = len(results)
                break              
             if entry[-1] == "*" and len(results) != count:                 
                results.append(entry[0:-1])
     
    return jsonify(results)


'''
Start the Application through cmd:
export FLASK_APP=<path to python file>/auto-complete_redis.py
flask run
'''
