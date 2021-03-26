from flask import Flask, request, jsonify, render_template
from facehandler import makeBlob, fromBlob, compare
from mysql.connector import connect, Error
from dbSeed import con, cur
from fileHandler import saveFile
from copy import deepcopy
import os


app = Flask(__name__)
ALLOWED_EXTENSIONS = ['png','jpg']
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# request body = groupname
@app.route('/addGroup', methods=['POST'])
def addG():
    req = request.json
    name = req['groupname']
    query = 'INSERT INTO groups(groupName) VALUES(%s)'
    try:
        cur.execute(query,name)
        con.commit()
    except Error as E:
        return jsonify({'error' : E})
    return 200,'succeed'

# request body = subgroupname, groupID
@app.route('/addSubgroup', methods=['POST'])
def addSG():
    req = request.json
    name = req['subgroupname']
    groupId = req['groupID']
    #database insert subgroup
    query = 'INSERT INTO subgroups(groupID,subgroupName) VALUES (%s,%s)'
    try:
        cur.execute(query,(groupId,name))
        con.commit()
    except Error as E:
        return jsonify({'error' : E})
    return "suceed"

#2. select list grup list subgrup
@app.route('/listGroup', methods=['GET'])
def listG():
    query = 'SELECT * FROM groups NATURAL JOIN subgroups'
    # try:
    cur.execute(query)
    temp = cur.fetchall()
    # except Error as E:
    #     return jsonify({'error' : E})
    return jsonify(temp)

# body = userid, role
@app.route('/signup', methods=['POST'])
def sign():
    req = request.json
    uname = req['userid']
    role = req['role']
    if role.lower() not in ['superuser','user']:
        return jsonify({'error' : "invalid role"})
    query = 'INSERT INTO user (username,role) VALUES (%s,%s)'
    try:
        cur.execute(query,(uname,role))
        con.commit()
    except Error as E:
        # print(E)
        return 500,jsonify({"error" : str(E)})
    return "succeed"


# body = id, subgrouptoenter
@app.route('/entersubgroup', methods=['POST'])
def enter():
    req = request.json
    query = 'INSERT INTO userinsubgroup VALUES (%s,%s)'
    try:
        cur.execute(query,(req['id'],req['subgroup']))
        con.commit()
    except Error as E:
        return E
    return "Success"

# request body = userid, name, imagefile, subgroupid
# returns success message
@app.route('/enroll', methods=['POST'])
def enroll():
    # role = 'Superuser'
    req  = request.form
    print(req)
    user = req['userid']
    imgfile = request.files['image'] 
    # toblob = request.files['image']
    # role = select role from database where userid = userid
    try:
        query = f"SELECT role FROM user WHERE username='{user}'"
        cur.execute(query)
    except Error as E:
        return str(E)
    role = cur.fetchall()
    # print(role[0][0])
    if role[0][0] != 'superuser':
        return jsonify({"error" : 401, "reason" : "Invalid role"})
    # blob = makeBlob(imgfile)
    # toblob = deepcopy(imgfile)
    # insert to database (subgroupid,name,blob)
    query = 'INSERT INTO encoding (subgroupID, faceOwner, encodingblob) VALUES (%s,%s,%s)'
    query2 = "UPDATE encoding SET encodingblob=%s WHERE faceID=%s"
    try:
        cur.execute(query,(req['subgroupid'],req['name'],""))
        lastid = cur.lastrowid
        saveFile(lastid, imgfile, req['name'], UPLOAD_FOLDER)  
        x = makeBlob(imgfile)
        cur.execute(query2,(x,lastid)) 
        con.commit()
    except Error as E:
        return jsonify({'error' : str(E)})
    return jsonify({"STATUS" : 200,"MESSAGE" : "succeed"})

# request body = imagefile, target subgroupid
@app.route('/recognize',methods=['POST'])
def recognize():
    req = request.form
    imgfile = request.files['image']
    # x = select from name,encodings where subgroupid =  req['subgroupid']
    try:
        query = f"SELECT faceOwner,encodingblob FROM encoding WHERE subgroupID='{req['subgroupid']}'"
        cur.execute(query)
    except Error as E:
        # print(E)
        return str(E)
    x = cur.fetchall()
    knownEncodings = []
    knownNames = []
    for i in x:
        knownEncodings.append(fromBlob(i[1])    )
        knownNames.append(i[0])
    print(knownNames)
    return jsonify({'Result' : compare(imgfile,knownEncodings,knownNames)})

@app.route('/selectFaces', methods=['GET'])
def selectFaces():
    req = request.args
    try:
        query = f"SELECT faceID, faceOwner FROM encoding WHERE subgroupID={req['subgrouid']}"
        cur.execute(query)
    except Error as E:
        print(E)
        return 'Err'
    data = cur.fetchall()
    mylist = []
    for i in data:
        mylist.append(i)
    return jsonify({'Result' : mylist})

@app.route('/deleteFace', methods=['GET'])
def selectFaces():
    req = request.args
    try:
        query2 = f"DELETE FROM images WHERE id={req['id']}"
        query = f"DELETE FROM encoding WHERE faceID={req['id']}"
        cur.execute(query2)
        cur.execute(query)
    except Error as E:
        print(E)
        return 'Err'
    con.commit()
    return "Succeed"

@app.route('/viewFace', methods=['GET'])
def view():
    req = request.args
    try:
        query = f"SELECT path FROM images WHERE id={req['faceid']}"
        cur.execute(query)
    except Error as E:
        return str(E)
    data = cur.fetchall()
    url = os.path.join(app.config['UPLOAD_FOLDER'],data[0][0].split('/')[-1])
    html = '''
    '''
    if data:
        # print('../'+data[0][0])
        return render_template('showimage.html',name=req['faceid'],user_image=url)
    else:
        return "Face not found"

if __name__ == '__main__':
    app.debug=True
    app.run(port=9000)
