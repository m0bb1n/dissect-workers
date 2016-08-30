import os

with open('/home/ubuntu/file_info.txt','w') as f:
    f.write(os.environ['FILE'])
