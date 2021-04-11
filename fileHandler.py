import os
from dbSeed import con, cur
from io import BytesIO

def allowed(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS


def saveFile(idF, imgfile, faceOwner, upload_folder, client):
    # if allowed(file.name):
    query = "INSERT INTO images(id, faceOwner, path) VALUES(%s,%s,%s)"
    cur.execute(query,(idF,faceOwner,faceOwner))
    con.commit()
    bytestr = imgfile.read()
    stream = BytesIO(bytestr)
    if client.bucket_exists("facerecimages"):
        pass
    else:
        client.make_bucket("facerecimages")
    client.put_object("facerecimages", faceOwner, stream, len(bytestr))
    # imgfile.save(path)
    # else:
        # raise jsonify({"Error" : })
        