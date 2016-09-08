import json
import os
import io
import requests
from mediafire import MediaFireApi, MediaFireUploader
from resource import CloudAccount
from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload

scopes = 'https://www.googleapis.com/auth/drive'
cs = '/home/deno/.client_secret.json'
appn = 'Dissect ALPHA'

class GoogleDrive (CloudAccount):
    def __init__ (self):


        flow = client.flow_from_clientsecrets(cs, scopes)
        flow.user_agent = appn

        #if flags:
        store = oauth2client.file.Storage('test.json')
        credentials = tools.run_flow(flow, store) #add flags at the end

        http = credentials.authorize(httplib2.Http())
        #print 'http:' + str(http)
        #print 'crenditital:' + str(credentials)
        self.cloud = discovery.build('drive', 'v3', http=http)

        #results = self.cloud.files().list(
        #    pageSize=10,fields="nextPageToken, files(id, name)").execute()

        #items = results.get('files', [])

        #if not items:
        #    print('No files found.')
        #else:
        #    print('Files:')
        #    for item in items:
        #        print('{0} ({1})'.format(item['name'], item['id']))

    def upload (self, FILE):
        #for f in FILE['parts']['googledrive']:
        if True:
            print 'starting upload'
            f={}
            f['id']='69'
            mimetype='application/octet-stream'
            f['path']='/home/deno/Downloads/gravity_2k-trailer.zip'
            media_body= MediaFileUpload(f['path'], mimetype=mimetype, resumable=True, chunksize=1024*1024)
            body= {
                'title':f['id'],
                'mimeType':mimetype
            }
            request=self.cloud.files().create(body=body, media_body=media_body).execute()
            f['cid']=request['id']
            print f['cid']
            #make a POST https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable

    def download(self, fileID):
        #for f in FILE['parts']['googledrive']:
        #    pass
        request = self.cloud.files().get_media(fileId=fileID)
        fh = io.FileIO('test.png','wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
                status, done = downloader.next_chunk()
                print "Download %d%%." % int(status.progress() * 100)

    def getStorageQuota (self):
        about = self.cloud.about().get(fields='storageQuota').execute()
        print about

class MediaFire (CloudAccount):
    def __init__ (self):
        self.auth = MediaFireApi()
        self.cloud = MediaFireUploader(self.auth)

    def upload (self, FILE):
        for f in FILE['parts']['mediafire']:
            fObject = open(f['partID'], 'rb')
            result = self.cloud.upload(fObject, FILE)
            print self.auth.file_get_info(result.quickkey)

    def download(self, FILE):
        for f in FILE['parts']['mediafire']:
            pass

test = GoogleDrive()
test.upload('sd')
