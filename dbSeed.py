from mysql.connector import connect, Error
from facehandler import makeBlob
import os

host = "127.0.0.1"
port = 3306
username = "rut"
password = "password"
database = "fr"

try:
    con = connect(host=host, port=port, user=username, password=password, db=database)
    cur = con.cursor()
except Error as E:
    print(E)


def insert(imgfile, subgroupid, name):
    encoding = makeBlob(imgfile)
    query = "INSERT INTO encodings VALUES (subgroupid, name, encoding)"
    cur.execute(query)
    con.commit()

def insertUser(username, role):
    query = "INSERT INTO users VALUES (username, role)"
    cur.execute(query)
    con.commit()


def seedtodb(foldername):
    queryG = f"INSERT INTO groups VALUES ({foldername.split('/')[-1].split(',')[0]},'{foldername.split('/')[-1].split(',')[1]}')"
    cur.execute(queryG)
    con.commit()
    # grouptoinsert = []
    sgtoinsert = []
    facetoinsert = []
    for subgroup in os.listdir(f"./{foldername}"):
        sgid,sgname = subgroup.split('.')[0].split(',')
        # querySG = "INSERT INTO subgroups VALUES (%d,%s)"
        # cur.execute(querySG,(int(sgid),sgname))
        # con.commit()
        sgtoinsert.append((int(sgid),foldername.split('/')[-1].split(',')[0],sgname))
        for names in os.listdir(f"./{foldername}/{subgroup}"):
            for files in os.listdir(f"./{foldername}/{subgroup}/{names}"):
                # img = files
                img = makeBlob(f"./{foldername}/{subgroup}/{names}/{files}")
                # query = "INSERT INTO encodings VALUES "
                facetoinsert.append((int(sgid),names,img))
    querySG = "INSERT INTO subGroups(subgroupID,groupID,subgroupName) VALUES (%s,%s,%s)"
    print(sgtoinsert)
    cur.executemany(querySG,sgtoinsert)
    con.commit()
    queryF = "INSERT INTO encoding (subgroupID,faceOwner,encodingblob) VALUES (%s,%s,%s)"
    cur.executemany(queryF,facetoinsert)
    con.commit()
    # print(sgtoinsert)
    # print(facetoinsert)
                