# import face_recognition
from face_recognition import load_image_file, face_encodings, compare_faces, face_locations
import numpy as np

# should be image file blob
def makeBlob(imagefile):
    image = load_image_file(imagefile)
    encoding = face_encodings(image)
    loc = face_locations(image)
    if len(loc) > 0:
        return np.array(encoding).tostring()
    else:
        return 'nah'

# def makeBlob(filename)
# returns feature vector
def fromBlob(blob):
    return np.frombuffer(blob, dtype=np.float64)

def compare(imgfile, knownEncodings, knownNames):
    try:
        image = load_image_file(imgfile)
        encoding = face_encodings(image)[0]
        matches = compare_faces(knownEncodings, encoding)
        print(matches)
        for match, name in zip(matches,knownNames):
            if match:
                return name
        return "unknown name"
    except:
        return "error"
