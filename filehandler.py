import subprocess
import os
from byteconvert import ByteConvert
import time
import boto3
import queuehandler
info=[]
with open("/home/deno/.aws_creds") as f:
    for line in f:
        info.append(line.replace('\n',''))
access_id = info[0]
access_secret = info[1]

class FileHandler (object):
    FILE = None
    s3 = None
    progressQueue=None
    def __init__(self, FILE):
        self.FILE=FILE
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=access_id,
            aws_secret_access_key=access_secret
        )
        self.DQ = queuehandler.DissectQueue()

    def prepare (self):
        self.FILE['path'] = '/home/deno/processing/{}/{}/'.format(self.FILE['user'],time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime()))
        self.FILE['FULL_PATH'] = self.FILE['path'] + self.FILE['id']
        prepare_command = 'mkdir -p {}'.format(self.FILE['path'])
        #subprocess.check_call(prepare_command)
        os.system(prepare_command)
        self.downloadFromS3()

    def downloadFromS3 (self):
        self.DQ.sendToUserQueue(self.FILE,10)
        with open(self.FILE['FULL_PATH'],'wb') as data:
            self.s3.download_fileobj(self.FILE['bucket'],self.FILE['id'], data)

    def process(self):

        self.findSplitSize()
        fileName = self.FILE['FULL_PATH']
        if self.FILE['compress']=='SM-7Z':
            fileName+='.7z'
            compress_7z_command = ['7z', 'a', fileName, self.FILE['FULL_PATH']]
            subprocess.check_call(compress_7z_command)

        splitName= fileName+'.'
        sizeandunit = str(self.FILE['split']['gcd']) + self.FILE['split']['unit']
        split_command = ['split', '--bytes', sizeandunit, '-d', '-a', '3', fileName, splitName]
        subprocess.check_call(split_command)

    def upload(self):
        pass
    def findSplitSize(self):
        self.FILE['size']=os.path.getsize(self.FILE['FULL_PATH'])
            # CLEANS THIS UP
        self.FILE['size']
        p=[]
        accountPercentage = [.30,.50,.20]
        for percent in accountPercentage:
            p.append(int(percent*self.FILE['size']))

        SMBC = ByteConvert(p)
        self.FILE['split']= SMBC.getBestUnit()
        print 'numbers=' + str(self.FILE['split']['numbers'])
        print 'gcd=' + str(self.FILE['split']['gcd'])
        for a in self.FILE['split']['numbers']:
            print str(a) + self.FILE['split']['unit'] +  ' that have ' + str(a/self.FILE['split']['gcd']) + ' files'

    def smartSplit(self):

        # calls a function in FileMovementHandler.py or some shit
        # basiclly calls a function to check the remaining space in each account
        #returns a dict.  The key is the account id, the value is the space following unit
        #FUCK MTY LIFE
        storage={34:'12g', 23:'12m',56:'2g'}

        #it will convert the all numbers into bytes


    def reset(self): #cleans up files to retry file compression
        reset_command = 'rm {}.*'.format(self.FILE['FILE_PATH'])
        subprocess.check_call(reset_command)


    def purge(self): #deletes folder and cleans file
        purge_command = 'rm -r {}*'.format(self.FILE['path'])
        subprocess.check_call(purge_command)


