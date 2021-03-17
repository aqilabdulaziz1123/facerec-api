# import face_recognition
from face_recognition import load_image_file, face_encodings, compare_faces
import numpy as np

# should be image file blob
def makeBlob(imagefile):
    image = load_image_file(imagefile)
    encoding = face_encodings(image)
    print(encoding)
    return np.array(encoding).tostring()


# returns feature vector
def fromBlob(blob):
    return np.frombuffer(blob, dtype=float64)

def compare(imgfile, knownEncodings, knownNames):
    image = load_image_file(imgfile)
    encoding = face_encodings(image)
    matches = compare_faces(knownEncodings, encoding)
    for match, name in zip(matches,knownNames):
        if match:
            return name
    return "unknown name"
    