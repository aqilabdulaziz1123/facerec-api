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
from flask_cors import CORS
from downloadHandler import aggregate_faces, download_by_url, video_to_audio, analyze_video, np_encoder, aggregate_text, aggregate_faces, reshape_faces
import json


app = Flask(__name__)
CORS(app)
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

# request body = subsubgroupname, subgroupID, groupID
@app.route('/addSubsubgroup', methods=['POST'])
# @jwt_required()
def addSSG():
    req = request.json
    name = req['subsubgroupname']
    groupId = req['groupID']
    subgroupId = req['subgroupID']
    query = 'INSERT INTO subsubgroups(groupID,subgroupID,subsubgroupName) VALUES (%s,%s,%s)'
    try:
        cur.execute(query,(groupId,subgroupId,name))
        con.commit()
    except Error as E:
        return jsonify({'error' : E})
    return "Succeed"

#2. select list grup list subgrup
@app.route('/listGroup', methods=['GET'])
# @jwt_required()
def listG():
    query=f'''
    SELECT groups.*, subgroups.subgroupID, subgroups.subgroupName, subsubgroups.subsubgroupID, subsubgroups.subsubgroupName
    FROM subgroups
    LEFT JOIN subsubgroups
    ON subgroups.subgroupID=subsubgroups.subgroupID
    RIGHT JOIN groups
    ON groups.groupID=subgroups.groupID
    '''
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

# request body = userid, name, image, subgroupid, subsubgroupid, groupid
# returns success message
@app.route('/enroll', methods=['POST'])
# @jwt_required()
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
    
    x = makeBlob(imgfile)
    if x == 'nah':
        return jsonify({'Result': 'Please Insert a Face'})
    
    try:
        query = 'INSERT INTO encoding (groupID, subgroupID, subsubgroupID, faceOwner, encodingblob) VALUES (%s,%s,%s,%s,%s)'
        query2 = "UPDATE encoding SET encodingblob=%s WHERE faceID=%s"
        cur.execute(query,(req['groupid'],req['subgroupid'],req['subsubgroupid'],req['name'], x))
        # lastid = cur.lastrowid
        # saveFile(lastid, imgfile, UPLOAD_FOLDER, client)  
        # imgfile.seek(0)
        # cur.execute(query2,(x,lastid)) 
        con.commit()
        # return jsonify({"last face id" : lastid})
        return 'Succeed'
    except Error as E:
        return jsonify({'error' : str(E)})

# request body = imagefile, target subgroupid
@app.route('/recognize',methods=['POST'])
# @jwt_required()
def recognize():
    req = request.form
    imgfile = request.files['image']
    try:
        query = f"SELECT faceOwner, encodingBlob FROM encoding WHERE groupID={req['groupid']}"
        cur.execute(query)
    except Error as E:
        return str(E)
    x = cur.fetchall()
    knownEncodings = []
    knownNames = []
    for i in x:
        knownEncodings.append(fromBlob(i[1]))
        knownNames.append(i[0])

    compared = compare(imgfile, knownEncodings, knownNames)
    if compared == 'unknown name':
        return jsonify({'Result': 'Unknown Face'})
    if compared == 'error':
        return jsonify({'Result': 'Please Insert a Face'})

    try:
        query2 = f'''
        SELECT groups.groupName, subgroups.subgroupName, subsubgroups.subsubgroupName
        FROM groups
        INNER JOIN subgroups
        ON groups.groupID=subgroups.groupID
        INNER JOIN subsubgroups
        ON subgroups.subgroupID=subsubgroups.subgroupID
        INNER JOIN encoding
        ON encoding.subsubgroupID=subsubgroups.subsubgroupID
        WHERE encoding.faceOwner=%(name)s
        '''
        cur.execute(query2, {'name': compared})
    except Error as E:
        return str(E)
    y = cur.fetchall()
    temp = []
    for i in y:
        temp.append(i)
    return jsonify({'Group': temp[0][0], 'Subgroup': temp[0][1], 'Subsubgroup': temp[0][2], 'Result': compared})

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


@app.route('/getFace', methods=['GET'])
def byteface():
    idF = request.args['id']
    if client.bucket_exists('facerecimages'):
        # try:
        query = f"SELECT path FROM images WHERE id={idF}"
        cur.execute(query)
        filetype = cur.fetchall()[0][0]
        if not filetype:
            return "id not found"
        resp = client.get_object('facerecimages',str(idF))
        byt = resp.data
        # print(byt)
        
        # KALO MAU NGESAVE JADI FILE LOCAL
        # stream = BytesIO(byt)
        # img = Image.open(stream)
        # img.save('test.jpg')
    else:
        return jsonify({"error" : "bucket not found"})
    return jsonify({"filetype" : filetype, "b64data" : str(byt)})

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

@app.route('/downloadOCR', methods=['GET'])
def downloadOCR():
    req = request.args
    try:
        video_path = download_by_url(req['url'])
        video_to_audio(video_path, 'audio')
        result = analyze_video(video_path)
        
        res_text = aggregate_text([i['text'] for i in result['result_feature']])
        result['agg_text'] = res_text

    except Error as E:
        return 'Err'
    return json.dumps(result, default=np_encoder)

@app.route('/downloadFace', methods=['GET'])
def downloadFace():
    req = request.args
    try:
        video_path = download_by_url(req['url'])
        result = analyze_video(video_path)
        
        res_face = aggregate_faces([i['faces_features'] for i in result['result_feature']])
        result['agg_faces'] = res_face

    except Error as E:
        return 'Err'
    return json.dumps(result, default=np_encoder)

if __name__ == '__main__':
    app.debug=True
    app.run(port=9000)
