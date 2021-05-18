import cv2
import glob
import face_recognition
from pytube import YouTube
import easyocr
import face_recognition
import json
import os
import moviepy.editor as mp
import time
import numpy as np
from Levenshtein import distance

reader = easyocr.Reader(['en'])

def download_by_url(vid_url,video_save_path="video",audio_save_path="audio"):
    vid = YouTube(vid_url)
    # download video only
    vid_stream = vid.streams.filter(file_extension = "mp4").get_highest_resolution()
    # print('downloading video..')
    vid_path = vid_stream.download(video_save_path)
    vid_json = {}
    vid_json["url"] = vid_url
    vid_json["res"] = vid_stream.resolution
    vid_json["mimetype"] = vid_stream.mime_type
    vid_json["fps"] = vid_stream.fps
    vid_json["filepath"] = vid_path
    jsonfile = video_save_path+"/"+vid_stream.default_filename[0:-3]+"json"
    with open(jsonfile, 'w') as f:
        f.write(json.dumps(vid_json))
    # print(vid_path, "downloaded")
 
    return vid_path

def video_to_audio(video_path, output_path):
    clip = mp.VideoFileClip("{}".format(video_path))
    filename = os.path.basename(video_path)[:-4] + '.wav'
    print("processing audio {}".format(filename))
    output_path = os.path.join(output_path, filename)
    clip.audio.write_audiofile("{}".format(output_path))
    print('{} is processed'.format(output_path))

def analyze_video(video, start_frame=0, end_frame=None, sampling_rate=1):
    """Find chicken dinner in video"""
    w, h, fps, num_frames = get_detail(video)
    print(w, h, fps, num_frames)
    start_frame = start_frame
    end_frame = end_frame if end_frame else num_frames
    step = int(round(sampling_rate * fps))
    start = time.time()
    cap = cv2.VideoCapture(video)
    i = start_frame
    output = []
    all_res = []
    while cap.isOpened() and i < end_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
#         print(i)
        ret, frame = cap.read()
#         print(frame)
#         try:
        temp_res = run_inference(frame)
#         except:
#             return frame
        all_res.append(temp_res)
        i += step
 
    cap.release()
    end = time.time()
 
    return {
        'start_frame' : start_frame,
        'end_frame' : end_frame,
        'result_feature': all_res,
        'step':step,
        'fps':fps
    }
 
def get_detail(vid_file):
    cap = cv2.VideoCapture(vid_file)
 
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
    cap.release()
 
    return width, height, fps, total_frames
 
def run_inference(frame):
    all_text_here = reader.readtext(frame) #OCR
    all_faces_locations = face_recognition.face_locations(frame)
     all_faces_features_here = face_recognition.face_encodings(frame)#FACE
    
    return {
        'text':all_text_here,
         'faces_location':all_faces_locations,
         'faces_features':all_faces_features_here
    }

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def distance_text(a,b):
    if max(len(a),len(b))==0:
        return 1
    return distance(a,b)/max(len(a),len(b))

def reshape_text(data1, data2, idx):
    for word in data2:
        used_word = word[1].lower()
        found = False
        for key in data1.keys():
            dist = distance_text(key,used_word)
            if dist<0.1:
                
                if data1[key][-1]['end']+1 == idx:
                    data1[key][-1]['end']+=1
                else:
                    data1[key].append({'start':idx, 'end':idx})
                found = True
                break
        if not found:
#             print('word : ',word[1].lower())
#             print(data1)
            data1[used_word] = [{'start':idx, 'end':idx}]
    return data1
    
def aggregate_text(all_text):
    aggregated_text = {}
    for idx,txt in enumerate(all_text):
        aggregated_text = reshape_text(aggregated_text,txt,idx)
    return aggregated_text

def reshape_faces(data1, data2, idx):
    for face1 in data2:
        found = False
        for k in data1.keys():
            dis = face_recognition.face_distance([data1[k]['face_image']] , face1)
            if dis<0.4:
                data1[k]['time'].append(idx)
                found=True
                break
        if not found:
            if len(data1.keys())>0:
                new_idx = max(list(data1.keys()))+1
            else:
                new_idx=0
            data1[new_idx] = {'face_image':face1,'time':[idx]}        
    return data1


def aggregate_faces(all_faces):
    aggregated_faces = {}
    for idx,faces in enumerate(all_faces):
        aggregated_faces = reshape_faces(aggregated_faces,faces,idx)
    return aggregated_faces
