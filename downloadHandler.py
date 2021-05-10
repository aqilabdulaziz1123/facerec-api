from pytube import YouTube
import json

def download_by_url(vid_url,video_save_path="video",audio_save_path="audio"):
    vid = YouTube(vid_url)
    # download video only
    vid_stream = vid.streams.filter(only_video=True, mime_type="video/mp4").order_by('resolution').desc().first()
    vid_path = vid_stream.download(video_save_path)
    vid_json = {}
    vid_json["url"] = vid_url
    vid_json["res"] = vid_stream.resolution
    vid_json["mimetype"] = vid_stream.mime_type
    vid_json["fps"] = vid_stream.fps
    vid_json["filepath"] = vid_path
    jsonfile = video_save_path+"/"+vid_stream.default_filename[0:-3]+"txt"
    with open(jsonfile, 'w') as f:
        f.write(json.dumps(vid_json))
    print(vid_path, "downloaded")
    # download audio only
    aud_stream = vid.streams.filter(only_audio=True,mime_type="audio/mp4").order_by('abr').desc().first()
    aud_path = aud_stream.download(audio_save_path)
    aud_json = {}
    aud_json["url"] = vid_url
    aud_json["bitrate"] = aud_stream.abr
    aud_json["mimetype"] = aud_stream.mime_type
    aud_json["filepath"] = aud_path
    jsonfile = audio_save_path+"/"+aud_stream.default_filename[0:-3]+"txt"
    with open(jsonfile, 'w') as f:
        f.write(json.dumps(aud_json))
    print(aud_path, "downloaded")