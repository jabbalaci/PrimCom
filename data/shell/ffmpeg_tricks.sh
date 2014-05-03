# replace audio track in a video
ffmpeg -i audio.mp3 -i video.mp4 -c copy final_video.mp4
