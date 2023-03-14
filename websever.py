from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from threading import Lock
from function.MethodParse import *
from function.response import *
import time
lock = Lock()

def accept_incoming_connections():
    """Sets up handling for incoming clients.""" 
    SERVER.listen(3) # Server cho phép tối đa 3 client vào trong hàng đợi
    while True:
        client, client_address = SERVER.accept() # Server chấp nhận kết nối từ client và bắt đầu trao đổi 
        lock.acquire()
        print("%s:%s has connected." % client_address)
        lock.release()
        addresses[client] = client_address
        thread = Thread(target=handle_client,args=(client,)) #Tạo thread xử lý trao đổi giữa client - server
        time.sleep(1)
        thread.start()
        
    
def handle_client(client):  
    """Handles a single client connection."""
    while True:
        try:
            name = client.recv(config.BUFSIZ).decode() # Nhận request từ client
            if not name: # Không nhận được request
                print(addresses[client] , " close")
                client.close()
                break

        except:
            client.close()
            break
        else:
            parseM = ParseMethod(name,addresses[client]) # Parse thông tin của request
            if parseM.empty == True:
                client.close()
                print(addresses[client], " close")
                break
            respond(client,parseM) # Phản hồi yêu cầu từ client
clients = {}
addresses = {}

ADDR = (config.HOST, config.PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    print("Waiting for connection...")
    accept_incoming_connections()
    ACCEPT_THREAD.join()
    SERVER.close()