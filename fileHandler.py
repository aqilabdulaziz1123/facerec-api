import os
from dbSeed import con, cur

def allowed(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS


def saveFile(idF, imgfile, faceOwner, upload_folder):
    # if allowed(file.name):
    path = os.path.join(f"images/{imgfile.filename}")
    query = "INSERT INTO images(id, faceOwner, path) VALUES(%s,%s,%s)"
    cur.execute(query,(idF,faceOwner,path))
    con.commit()
    imgfile.save(path)
    # else:
        # raise jsonify({"Error" : })
        