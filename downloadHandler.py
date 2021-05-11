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
    # all_faces_locations = face_recognition.face_locations(frame)
    # all_faces_features_here = face_recognition.face_encodings(frame)#FACE
    
    return {
        'text':all_text_here,
        # 'faces_location':all_faces_locations,
        # 'faces_features':all_faces_features_here
    }

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()