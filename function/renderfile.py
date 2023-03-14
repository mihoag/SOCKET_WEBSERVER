def _read_file(namefile):
    try:
         f = open(namefile,'rb')
         return f.read()
    except:
        return "error"
        
def _renderFile(filename, type = 1): # filename tồn tại trả về thành công "200 OK" và render file
    head = ''
    head += "HTTP/1.1 200 OK\r\n"
    head += "Connection: keep-alive\r\n" # Giữ kết nối 
    if(type == 1 ):
        head += "Keep-Alive: timeout=30, max=10\r\n" # set timeout = 30s và cho phép gửi tối đa 30 request 
        head += 'Content-Type: Text/html\r\n'
    elif type == 2:
        head += "Keep-Alive: timeout=30, max=10\r\n"
        head +=  'Content-Type: image/*\r\n'
    elif type == 3:
        head += "Keep-Alive: timeout=30, max=10\r\n"
        head += 'Content-Type: text/css\r\n'
    elif type == 4:
        head += "Keep-Alive: timeout=30, max=10\r\n"
        head += 'Content-Type: image/x-ico\r\n'
    content = _read_file(filename)
    if content == "error":
        return "error"
    head += "Content-Length: %d\r\n\r\n" %len(content)
    return head.encode('utf-8') + content + "\r\n".encode('utf-8')

