import argparse
from importlib.resources import open_binary
import socket
import queue
from threading import Thread, Lock
from tracemalloc import start
from turtle import end_fill
import time

class Port_Scanner():
    def __init__(self, host, start, end, threads):
        self.host = host #server IP
        self.start_port = start
        self.end_port = end
        self.port_range = queue.LifoQueue() #port queue for multithread
        self.threads = threads #number of threads
        self.lock = Lock() #support output layout, will increase processing time
        self.open_port = [] #Saving the ports that are open

    def is_port_open(self, port):
        s = socket.socket()

        try:
            s.connect((self.host,port))
            s.settimeout(0.2)
        except:
            #can't connect -> port is closed
            return False
        else:
            #port is open :D
            return True
        finally:
            s.close()
    
    def fill_port(self):
        port_list = list(range(self.start_port, self.end_port+1))
        port_list.reverse()
        for _ in port_list:
            self.port_range.put(_)

    def network_scan(self):
        #main
        self.fill_port()

        thread_list = []
        for i in range(1,self.threads+1):
            thread = Thread(target=self.port_scan) 
            thread.daemon = True
            thread.start()
            thread_list.append(thread)       

        for thread in thread_list:
            thread.join()

    def port_scan(self):
        # For output layout support, uncomment as needed.
        #self.lock.acquire()
        while not self.port_range.empty():
            current_port = self.port_range.get()
            open = self.is_port_open(current_port)
            if open:  
                print("%s: %d is open" %(self.host,current_port))
                self.open_port.append(current_port)
                #print("%s: %d is open" %(self.host,current_port))
            else:
                print("%s: %d is closed" %(self.host,current_port))
                #print("%s: %d is closed" %(self.host,current_port))

        # For output layout support, uncomment as needed.
        #self.lock.release()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',
                        help='Server IP')      
    parser.add_argument('starting',
                        type=int, 
                        help='Starting port',
                        nargs='?',
                        default=1)  
    parser.add_argument('ending',
                        type=int, 
                        help='Ending port',
                        nargs='?',
                        default=1024) 
    parser.add_argument('threads',
                        type=int,
                        help='Number of threads', 
                        nargs='?',
                        default=50)
    return parser.parse_args()

if __name__ == '__main__':
    start_time = time.time()

    args = parse_args()
    host = args.host
    start_port = args.starting
    end_port = args.ending
    threads = args.threads

    scanner = Port_Scanner(host, start_port, end_port, threads)
    scanner.network_scan()
    end_time = time.time()

    open_port = scanner.open_port
    print("\nOpen port(s):")
    for _ in range(0,len(open_port)):
        print(open_port[_])
    print('\nTime taken: %.3fs' %(end_time-start_time))

