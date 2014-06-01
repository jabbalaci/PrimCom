/opt/ffmpeg/ffmpeg -i "input.ogv" -codec:v libx264 -quality good -cpu-used 0 -profile:v baseline -level 30 -y -maxrate 2000k -bufsize 2000k -threads 4 -codec:a copy -b:a 128k "output.mp4"
