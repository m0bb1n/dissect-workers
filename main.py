import json
from filehandler import FileHandler
import boto3
import time
from heartbeat import HeartbeatSocket
import thread
import os

class DissectWorker(object):
    FILE = None
    progressQueue = None

    def __init__ (self):
        #with open('FILE_info','r') as f:
            #self.FILE=json.loads(f.read())
        #self.progressQueue = self.sqs.Queue(self.FILE['queue_url'])
        self.FILE={'name':'test'}
        #self.FILE=json.loads(os.environ['FILE'])

    def start (self):
        while self.checkForFile() is not True:
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
                },
                'percent': {
                    'StringValue': str(percent),
                    'DataType': 'String'
                }
            }
        )


if __name__ == "__main__":
    thread.start_new_thread(HeartbeatSocket(os.environ['manager_url'],9999).listenForClient,())
    DW = DissectWorker()
    DW.start()
    ### FINISHES DOING EVERYTHING AND THEN TERMINATES ITSELF
