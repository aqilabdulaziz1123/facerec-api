from flask import Flask, request, jsonify
from facehandler import makeBlob, fromBlob, compare


app = Flask(__name__)

# request body = groupname, array berisi daftar subgroupname minimal berisi 1
@app.route('/addGroup', methods=['POST'])
def addG():
    req = request.json
    name = req['groupname']
    for i in req['subs']:
        #insertsub to db
        pass
    return 200,'succeed'

# request body = subgroupname, groupID
@app.route('/addSubgroup', methods=['POST'])
def addSG():
    req = request.json
    name = req['subgroupname']
    groupId = req['groupID']
    #database insert subgroup
    return "suceed"

# body = userid, role, array of subgroupIDs
@app.route('/signup', methods=['POST'])
def sign():
    req = request.json
    uname = req['userid']
    role = req['role']
    if role not in ['Superuser','User']:
        return "invalid role"
    #database insert user
    return "succeed"

# request body = userid, name, imagefile, subgroupid
# returns success message
@app.route('/enroll', methods=['POST'])
def enroll():
        role = 'Superuser'
        # role = select role from database where userid = userid
        if role is not 'Superuser':
            return 401,"Invalid role"
        req = request.json
        imgfile = request.form['image']
        blob = makeBlob(imgfile)
        # insert to database (subgroupid,name,blob)
        return 200, "succeed"

# request body = userid, imagefile, target subgroupid, 
@app.route('/recognize',methods=['POST'])
def recognize():
    req = request.json
    imgfile = request.form['image']
    x = []
    # x = select from name,encodings where subgroupid =  req['subgroupid']
    knownEncodings = []
    knownNames = []
    for i in x:
        knownEncodings.append(i[1])
        knownNames.append(i[0])
    return jsonify({'Result' : compare(imgfile,knownEncodings,knownNames)})


@app.route('/tesimagefile', methods=['POST'])
def printa():
    print('hai')
    print(request.files['file'])
    print(makeBlob(request.files['file']))
    # req = request.json
    # print(req)
    # imgfile = request.form['file']
    # print(imgfile)
    return jsonify({'hi' : 'fagt'})



app.run()