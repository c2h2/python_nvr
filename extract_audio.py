import glob
import os
import datetime

files_location = "/var/www/nvr/"

all_files = glob.glob(files_location + "*.mkv")

for f in all_files:
    current_time = datetime.datetime.now()
    file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(f))
    time_difference = current_time - file_mod_time
    opusfile = os.path.splitext(f)[0] + '.opus'

    #remove old empty files
    if os.path.isfile(f):
        if os.path.getsize(f) < 1000:         
            
            if (time_difference).days >= 1:
                print(f + " is empty and >1 day old, deleting")
                os.remove(f)
            continue

    # skip if the file too new
    if time_difference < timedelta(hours=2):
        continue
    
    # skip if the opus file already exists and is not empty
    if os.path.exists(opusfile):
        if os.path.getsize(opusfile) > 1000:
            continue
    
    cmd = 'ffmpeg -y -i ' + f + ' -vn -ac 1 -ar 8000 -acodec libopus -b:a 64k ' + opusfile
    print(cmd)
    os.system(cmd)

