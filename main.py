import json
import os
from filehandler import FileHandler
import boto3
import time

class DissectWorker(object):
    FILE = None
    progressQueue = None

    def __init__ (self):
        with open('FILE_info','r') as f:
            self.FILE=json.loads(f.read())
        self.progressQueue = self.sqs.Queue(FILE['queue_url'])


    def start (self):
        self.FILE=
        while !checkForFile():
            time.sleep(2)

    def checkForFile (self):
        return os.path.isfile('/file/'+self.FILE['name'])

    def sendToUserQueue(self,stage,percent): #send the progress to user queue which is then read by web services
            self.progressQueue.send_message(
            MessageBody='message',
            DelaySeconds=0,
            MessageAttributes={
                'stage': {
                    'StringValue': stage,
                    'DataType': 'String'
                }
                'percent': {
                    'StringValue': str(percent),
                    'DataType': 'String'
                }
            }
        )



if __name__ == "__main__":
    DW = DissectWorker()
    DW.start()

