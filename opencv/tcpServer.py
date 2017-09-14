#python3

import socket
import sys
import json
HOST = '' #all available interfaces
PORT = 7777

#1. open Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#2. bind to a address and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#3. Listen for incoming connections
s.listen(100)
print ('Socket now listening')


def main():
    while True:
	#접속 승인
        conn, addr = s.accept()
        print("Connected by ", addr)
    
        #데이터 수신
        data = conn.recv(1024)
        data = data.decode("utf8").strip()
        if not data: break
        print("Received: " + data)

    
        #수신한 데이터로 파이를 컨트롤 
        if int(data) == 1:
            print('json 읽기')
            f = open('1.json', 'r')
            res = f.readline()
            print(type(res))
            conn.sendall(res.encode("utf-8"))
            conn.close()
        elif int(data) == 2:
            print('input 2, shutdown')
            conn.close()
            break
        else:
            print("파이 입력 :" + data)
            conn.sendall(data.encode("utf-8"))
            conn.close()
        
        #클라이언트에게 답을 보냄
#        conn.sendall(res.encode("utf-8"))
	    #연결 닫기
#        conn.close()
    



try:
    main()
except:
    s.close()
    print('server shutdown')
