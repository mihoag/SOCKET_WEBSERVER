import config
from threading import Lock
lock = Lock()

class ParseMethod: # Parse request từ client
    def __init__(self, request,client):
        self.request = request
        if request == '':
            self.empty = True
            return
        else:
            request_line = str(request).split('\n')
            self.empty = False
            self.method = request_line[0].split(' ')[0]
            self.path =request_line[0].split(' ')[1]
            self.content = request_line[-1]
            #lock.acquire()
            print("client :" ,client , " : " , self.method," ", self.path)
            #lock.release()
            