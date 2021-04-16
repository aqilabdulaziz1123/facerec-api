import os
from dbSeed import con, cur
from io import BytesIO, StringIO
from base64 import b64decode, b64encode

def allowed(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS


def saveFile(idF, imgfile, upload_folder, client):
    # if allowed(file.name):
    # filetype = imgfile.name.split('.')[-1]
    # images tadinya ga kepake, skrg dibuat nyimpen filetype
    query = "INSERT INTO images(id, faceOwner, path) VALUES(%s,%s,%s)"
    cur.execute(query,(idF,"",imgfile.filename.split('.')[-1]))
    con.commit()
    bytestr = imgfile.read()
    # stream = BytesIO(bytestr)
    streamdata = b64encode(str(bytestr).encode('utf-8'))
    stream = BytesIO(streamdata)
    # stream = StringIO(streamdata)
    if client.bucket_exists("facerecimages"):
        pass
    else:
        client.make_bucket("facerecimages")
    client.put_object("facerecimages", str(idF), stream, len(bytestr))
    # imgfile.save(path)
    # else:
        # raise jsonify({"Error" : })
        