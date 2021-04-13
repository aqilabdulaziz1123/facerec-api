from flask import Flask, request, jsonify, render_template
from facehandler import makeBlob, fromBlob, compare
from mysql.connector import connect, Error
from dbSeed import con, cur
from fileHandler import saveFile
from copy import deepcopy
import os
from flask_httpauth import HTTPBasicAuth
from minio import Minio
from minio.error import S3Error
from sys import getsizeof
from PIL import Image
from io import BytesIO
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secreto"
jwt = JWTManager(app)
ALLOWED_EXTENSIONS = ['png','jpg']
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = Minio( 
    "play.min.io", #ini kudu diganti keknya karena ini cuma buat trial gitu
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
)

@app.route("/getToken", methods=['GET'])
def getToken():
    # add login later if needed
    return jsonify(token=create_access_token(identity="admin"),howto="tambahin header 'Authorization' trus valuenya 'Bearer *tokennya   *'")


# request body = groupname
@app.route('/addGroup', methods=['POST'])
@jwt_required()
def addG():
    req = request.json
    name = req['groupname']
    query = f"INSERT INTO groups(groupName) VALUES('{name}')"
    try:
        cur.execute(query)
        con.commit()
    except Error as E:
        return jsonify({'error' : str(E)})
    return jsonify({"user" : get_jwt_identity(), "result" : "Succeed"})

# request body = subgroupname, groupID
@app.route('/addSubgroup', methods=['POST'])
@jwt_required()
def addSG():
    req = request.json
    name = req['subgroupname']
    groupId = req['groupID']
    query = 'INSERT INTO subgroups(groupID,subgroupName) VALUES (%s,%s)'
    try:
        cur.execute(query,(groupId,name))
        con.commit()
    except Error as E:
        return jsonify({'error' : E})
    return "suceed"

#2. select list grup list subgrup
@app.route('/listGroup', methods=['GET'])
# @jwt_required()
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
@jwt_required()
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
@jwt_required()
def enroll():
    # role = 'Superuser'
    req  = request.form
    print(req)
    user = req['userid']
    imgfile = request.files['image'] 
    try:
        query = f"SELECT role FROM user WHERE username='{user}'"
        cur.execute(query)
    except Error as E:
        return str(E)
    role = cur.fetchall()
    if role[0][0] != 'superuser':
        return jsonify({"error" : 401, "reason" : "Invalid role"})
    query = 'INSERT INTO encoding (subgroupID, faceOwner, encodingblob) VALUES (%s,%s,%s)'
    query2 = "UPDATE encoding SET encodingblob=%s WHERE faceID=%s"
    try:
        cur.execute(query,(req['subgroupid'],req['name'],""))
        lastid = cur.lastrowid
        saveFile(lastid, imgfile, req['name'], UPLOAD_FOLDER, client)  
        imgfile.seek(0)
        x = makeBlob(imgfile)
        cur.execute(query2,(x,lastid)) 
        con.commit()
    except Error as E:
        return jsonify({'error' : str(E)})
    return jsonify({"STATUS" : 200,"MESSAGE" : "succeed"})

# request body = imagefile, target subgroupid
@app.route('/recognize',methods=['POST'])
@jwt_required()
def recognize():
    req = request.form
    imgfile = request.files['image']
    try:
        query = f"SELECT faceOwner,encodingblob FROM encoding WHERE subgroupID={req['subgroupid']}"
        cur.execute(query)
    except Error as E:
        # print(E)
        return str(E)
    x = cur.fetchall()
    # print(x.shape)
    print(len(x))
    # print(len(x[0]))
    # knownEncodings = np.array([[]])
    knownEncodings = []
    knownNames = []
    for i in x:
        # if i:
            # knownEncodings.append(fromBlob(i[1]))
            # knownNames.append(i[0])
        res = compare(imgfile, [fromBlob(i[1])],[i[0]])
        if res != 'unknown name':
            return res
    return jsonify({'Result' : res})

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
def deleteface():
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
    return "Succeed "

@app.route('/viewFace', methods=['GET'])
def view():
    filename = request.args['filename']
    if client.bucket_exists('facerecimages'):
        resp = client.get_object('facerecimages',filename)
        byt = resp.data
        print(byt)
        stream = BytesIO(byt)
        img = Image.open(stream)
        img.save('test.jpg')
        # x = resp.read(decode_content=True)
        # print(x)
    else:
        return "bucket not found"
    return render_template("showimage.html",name=filename,user_image='test.jpg')

@app.route('/tesminio', methods=['GET','POST'])
def minio():
    if request.method == 'POST':
        req  = request.form
        user = req['userid']
        imgfile = request.files['image']
        x = getsizeof(imgfile)
        bytestr = imgfile.read()
        print(bytestr)
        stream = BytesIO(bytestr)
        name = req['name']
        if client.bucket_exists("facerecimages"):
            pass
        else:
            client.make_bucket("facerecimages")
        client.put_object("facerecimages", name, stream, len(bytestr))
    elif request.method == 'GET':
        filename = request.args['filename']
        if client.bucket_exists('facerecimages'):
            resp = client.get_object('facerecimages',filename)
            byt = resp.data
            print(byt)
            stream = BytesIO(byt)
            img = Image.open(stream)
            img.save('test.jpg')
            # x = resp.read(decode_content=True)
            # print(x)
        else:
            return "bucket not found"
        return "done"

    
    # try:
    #     query = f"SELECT role FROM user WHERE username='{user}'"
    #     cur.execute(query)
    # except Error as E:
    #     return str(E)
    # role = cur.fetchall()
    # if role[0][0] != 'superuser':
    #     return jsonify({"error" : 401, "reason" : "Invalid role"})
    # query = 'INSERT INTO encoding (subgroupID, faceOwner, encodingblob) VALUES (%s,%s,%s)'
    # query2 = "UPDATE encoding SET encodingblob=%s WHERE faceID=%s"
    # try:
    #     cur.execute(query,(req['subgroupid'],req['name'],""))
    #     lastid = cur.lastrowid
    #     saveFile(lastid, imgfile, req['name'], UPLOAD_FOLDER)  
    #     x = makeBlob(imgfile)
    #     cur.execute(query2,(x,lastid)) 
    #     # con.commit()
    # except Error as E:
    #     return jsonify({'error' : str(E)})
    return jsonify({"STATUS" : 200,"MESSAGE" : "succeed"})


if __name__ == '__main__':
    app.debug=True
    app.run(port=9000)
