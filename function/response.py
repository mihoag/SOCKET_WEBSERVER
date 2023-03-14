import config
from function.renderfile import *
from function.renderfile import _renderFile

# Kiểm tra thông tin đăng nhập từ phía client
def checkInfo(content): 
    user = ''
    pas = ''
    com = str(content).split('&',maxsplit=2)
    
    getuser = com[0].split('=')
    user = getuser[1]

    getpass = com[1].split('=')
    passw = getpass[1]

    if(user ==  config.user and passw == config.passw):
        return True
    return False

def responseError(client): # Phản hồi 404 Not Found nếu client yêu cầu filename không tồn tại
    data = "<!DOCTYPE html> <html> <head> <title> 404 Not Found </title> </head> <body> <p> The requested file cannot be found. </p> </body> </html>"
    msg = "HTTP/1.1 404 Not Found\r\n"+"Content-Type: text/html\r\n"+ "Connection: close\r\n" + "Content-Length:"+ str(len(data))+ "\r\n\r\n" + data
    client.send(bytes(msg, "utf8"))
    return
    
def respond(client,parseM): # Phản hồi cho request từ client
    path = str(parseM.path).split('/',maxsplit = 1)
    path1 = ''
    path1 = path[1]
    # Xác định tên và loại file cần respond cho client (.html, .css, .png/.jpg)
    typecode = 0
    typefile = ''
    if path1 == '':
        typecode = 1
    else:
        typefile = path1.split('.')
        elements=len(typefile)
        if(elements==2):
            if typefile[1] == 'html':
                typecode = 1
                path1='page/'+path1
            elif typefile[1] == 'css':
                typecode = 3
            elif typefile[1] == 'png' or typefile[1] == 'jpg':
                typecode = 2
            else:
                 responseError(client)
                 return 
        else:
            responseError(client)
            return

    if(parseM.method == 'GET'): # Client GET request
        if(path1 == ''):
            res = _renderFile('page/index.html',1)
            client.send(bytes(res))

        elif(path1=='page/images.html'):
            try:
                checkInfo(parseM.content)
            except:
                responseError(client)          # method GET request đến images.html thì respond error
        else:
            res = _renderFile(path1,typecode)
            if(res != "error"):
                client.send(bytes(res))
            else:
                responseError(client)
             
    elif(parseM.method == 'POST'): # Client đăng nhập
        if checkInfo(parseM.content):
            res = _renderFile(path1,typecode)
            client.send(bytes(res))
        else:
                data = "<h1>401 Unauthorized</h1> <p>This is a private area.</p>"
                msg = "HTTP/1.1 401 Unauthorized\r\n"+"Content-Type: text/html\r\n" +"Connection: close\r\n"+ "Content-Length:"+ str(len(data))+ "\r\n\r\n" + data
                client.sendall(bytes(msg, "utf8"))
    else:
        responseError(client)
