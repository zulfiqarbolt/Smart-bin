

#--- IMPORT DEPENDENCIES ------------------------------------------------------+
import PSOTEST as pt
import math
from random import randint
import sys
import requests
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json
from math import sin, cos, sqrt, atan2, radians
from flask_cors import CORS, cross_origin


cf_deployment_tracker.track()







#--- Test ---------------------------------------------------------------------+

from random import randint

global nlist
nlist=[]
global minbin
minbin=[]
global mincbin
mincbin=[]

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyCncJtRmHn7tGptHCZvciuvvGlqoqpdltk')










app = Flask(__name__)
CORS(app)
db_name = 'sbldb'
client = None
db = None


user = "bca1f626-e7b3-47fa-9c9d-f9ab9a9aef3f-bluemix"
password = "702d15efb526b9b22c7442f3e1d6523defbc7f1666848bdbdfcdaaa6d1815104"
url = "https://bca1f626-e7b3-47fa-9c9d-f9ab9a9aef3f-bluemix:702d15efb526b9b22c7442f3e1d6523defbc7f1666848bdbdfcdaaa6d1815104@bca1f626-e7b3-47fa-9c9d-f9ab9a9aef3f-bluemix.cloudant.com"
client = Cloudant(user, password, url=url, connect=True)
db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('out.html')
@app.route('/api/sim')
def sim():
    return render_template('mappp.html')


@app.route('/api/createbin/<ids>/<lat>/<lng>/<cont>/<moist>/<count>')
def createbin(ids,lat,lng,cont,moist,count):
    if client:
        data = {
            "_id":ids,
            "lat":lat,
            "lng":lng,
            "count":count,
            "moisture":moist,
            "content":cont
        }
        db.create_document(data)
        return 'Container Created' 
    else:
        return 'Unable to create Bin'


@app.route('/api/updatebin/<ids>/<lat>/<lng>/<count>/<moist>/<cont>')
def updatebin(ids,lat,lng,count,moist,cont):
    
    if client:
        f=0

        for my_document in db:
            if(my_document['_id']==str(ids)):
                                       my_document['content'] = cont
                                       my_document['moisture'] = moist
                                       my_document['count'] = count
                                       my_document['lat'] = lat
                                       my_document['lng'] = lng
                                       my_document.save()
                                       f=1
        if f==0:
            return 'No Container Found'
        return 'Container Updated' 
    else:
        return 'Unable to Update Container'


@app.route('/api/removebin/<lat>/<lng>')
def removebin(lat,lng):
    
    if client:
        f=0

        for my_document in db:
            if(my_document['lat']==str(lat) and my_document['lng']==str(lng)):
                                            my_document.delete()
                                            f=1
        if f==0:
            return 'No Container Found'
        return 'Container Removed' 
    else:
        return 'Unable to Remove Bin'







@app.route('/api/nearbin/<lat>/<lng>/<rad>')
def nearbin(lat,lng,rad):
    data=[]
    global minbin
    minbin=[]
    global mincbin
    mincbin=[]
    maxV=float(rad)
    maxcV=101

    for my_document in db:
                    orig_coord = str(my_document['lat'])+","+ str(my_document['lng'])
                    dest_coord = str(lat)+","+ str(lng)
                    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
                    r = requests.get(url)
                    result= r.json()
                    dis = result['rows'][0]['elements'][0]['distance']['text']
                    dist= dis.split()
                    mv=float(dist[0])
                    mk=(float(my_document['moisture'])+float(my_document['content']))/2
                    print mv
                    if float(rad) >= mv:
                        if maxV>mv:
                            maxV=mv
                            minbin=my_document
                        if maxcV>mk:
                            maxcV=mk
                            mincbin=my_document                          
                            
                        data.append(my_document)
                    

    return jsonify({1:[data],2:[minbin],3:[mincbin]})
  






@app.route('/api/locate')
def locate():
    data=[]
    for md in db:
        data.append(md)
    return jsonify(data)


@app.route('/api/remove/all')
def removeall():
    data=[]
    for md in db:
        md.delete()
    for md in db:
        md.delete()
    return "Deleted"




@app.route('/api/test')
def test():
    r = requests.get('https://smartbinlog.mybluemix.net/api/locate')
    data= r.json()
    lt=0
    for d in data:
        lt=lt+1
    for d in data:
        print d["_id"]
    return "u"




    
@app.route('/api/flow/<bt>')
def flow(bt):
    global nlist
    containers = []
    containers2 = []
    containers_bincount = []
    lst=[]
    r = requests.get('https://smartbinlog.mybluemix.net/api/locate')
    data= r.json()
    bc=int(data[0]['count'])
    lt=0
    for d in data:
        lt=lt+1


    for i in range(0,lt):
        containers.append([])
        containers2.append([])
        containers_bincount.append(bc)
        lst.append([])
    cnti=0
    for d in data:
            #print d["_id"]
            a=int(d["content"])
            b=int(d["moisture"])
        
            containers[cnti].append(a)
            containers[cnti].append(b)        
            containers[cnti].append(cnti)        
            containers[cnti].append(bc)
            containers[cnti].append(d["lat"])        
            containers[cnti].append(d["lng"]) 
                    
            lst[cnti].append(cnti) 
            lst[cnti].append(d["lat"])        
            lst[cnti].append(d["lng"])        
            lst[cnti].append(0)
            lst[cnti].append(0)         
            lst[cnti].append(bc)
            if (a+b)/2>=int(bt):
                lst[cnti].append(1)
            else:
                lst[cnti].append(0)
            
        
            lst[cnti].append(a)
            lst[cnti].append(b) 
            lst[cnti].append(0) 
            lst[cnti].append('')
            lst[cnti].append('') 
                
            
            
            containers2[cnti].append(100-a)
            containers2[cnti].append(100-b)        
            containers2[cnti].append(cnti)        
            containers2[cnti].append(bc)
            cnti=cnti+1
    
    
    lst=pt.psofit(containers,containers2,containers_bincount,bc,lt,lst)
    nlist=[]
    ncnt=0
    nv=[]
    for d in lst:
        if int(d[6])==1:
            nlist.append(d)
            ncnt=ncnt+1
    st=0
    ed=0
    sg=''
    for i in range(0,ncnt):
        maxv = float('inf')
        maxi=-1


        
        for j in range(0,ncnt):
            if(st!=j):
                ed=j
                if j in set(nv):
                    ju=0
                else:




                    orig_coord = str(nlist[st][1])+","+ str(nlist[st][2])
                    dest_coord = str(nlist[ed][1])+","+ str(nlist[ed][2])
                    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
                    r = requests.get(url)
                    result= r.json()
                    dis = result['rows'][0]['elements'][0]['distance']['text']
                    dist= dis.split()
                    sg+='Distance to '+str(nlist[ed][0])+' : '+dis+'\n'
                    mv=float(dist[0])
                    if maxv > mv:

                        maxv=mv
                        maxi=ed


        
        nv.append(st)
        nlist[st][10]=sg
        st=maxi
        print st
        sg=''
        



    for i in range(0,len(nv)):
        nlist[int(nv[i])][9]= str(i)
        if(i+1<len(nv)):
            nlist[int(nv[i])][11]= "Next Bin : "+str(nlist[int(nv[i+1])][0])
        else:
            nlist[int(nv[i])][11]= "Last Bin  "
        print str(nv[i])+ " " + str(i)
    return jsonify(lst)




    
@app.route('/api/flow/route')
def route():
    global nlist
    return jsonify(nlist)


               
@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port,threaded=True)
