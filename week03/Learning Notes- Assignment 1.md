# Learning Notes: Assignment 1

## Version 1. Single Threaded Port Scanner

Reference: [Python For Penetration Testing - Developing A Port Scanner](https://www.youtube.com/watch?v=d3D8PAZV51g)

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5) # five seconds

# set a host which we are going to use
host = '104.193.88.77'
port = 443

def port_scanner(host, port):
    if s.connect_ex((host, port)):
        print('The port is closed.')
    else:
        print('The port is open.')

port_scanner(host, port)

# output: The port is open.
```

However, if we try port = other numbers, it is not neccessary that the output will appear that soon. For example:

![](pic/slow_port_output.png)

Therefore, it is necessary to set the timeout parameter.


## Version 1.1 Single Threaded Port Scanner

Reference: [Building a port scanner in python](https://medium.com/@itsnee/building-a-port-scanner-in-python-61b253dbc9f6)

```python
import argparse
from sys import argv, exit
import socket
from datetime import datetime as dt

# 0. 
def new_line():
    print('\n') #prints new line when function is called


# 1. Define our target
# If the number of arguments entered matches the number of arguments we require, 
# we let the program continue
# Else, we alert the user that the input was invalid

# Checks if there are only 2 arguments entered (e.g. assignment1.py www.baidu.com)
if len(argv) == 2:
    target = socket.gethostbyname(argv[1]) # DNS
    # Add a pretty banner
    new_line()
    print('-'* 50)
    print('scanning host: {}'.format(target))
    print('Time started: {}'.format(dt.now()))
    print('-' * 50)
    new_line()
    # 104.193.88.123 if I typed in the terminal: python3 assignment1.py www.baidu.com
else:
    new_line()
    print('Invalid number of arguments entered.')
    print('Syntax should be: python3 portscanner.py <website address>')
    new_line()


# Create a try statement to scan ports on the target machine
try:
    open_port_list = []
    port_num_range = range(21, 81)
    for port in port_num_range:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1) # Ends connection if a port does not respond in 1 second
        result = s.connect_ex((target, port))
        # returns an error indicator; open port==0, closed port==1
        if result == 0:
            print('Port {} is open and unfiltered'.format(port))
            open_port_list.append(port)
            new_line()
    print('Successfully scanned {} ports, and {} ports are open.'.format(
        len(port_num_range), len(open_port_list)
    ))
    s.close
    print('-' * 25 + ' end ' + '-' * 25)

except KeyboardInterrupt:
    print('Terminating Scan.')
    exit()

except socket.gaierror:
    print('Hostname could not be resolved.')
    exit()
    
except socket.gaierror:
    print('Could not connect to the server. ')
    exit()

```

Test:

```python

python3 assignment1.py www.baidu.com

--------------------------------------------------
scanning host: 104.193.88.77
Time started: 2020-07-10 11:20:16.793004
--------------------------------------------------


Port 80 is open and unfiltered


Successfully scanned 60 ports, and 1 ports are open.
------------------------- end -------------------------
```

## Version 1.2 Single Threaded Port Scanner with More Parameters

Implemented more parameters based on the Version 1.1.

1. Traced how much time the program will take, which is more than only claiming the time from which the program starts.
2. Existing parameters: (1) -url the_web_link
3. More parameters: (2) -method ping/tcp (3) -start start_port_num (4) -end end_port_num (5) -w result.json (6) -v (printing how much time the program has spent)
4. Checked whether the parameters are correct in terms of their own formats.

```python
import argparse
from sys import argv, exit
import socket
from time import time
import json
import os


class PortScanner(object):
    '''
    Parameters:
    (1) -url the_web_link
    (2) -method ping/tcp
    (3) -start start_port_num 
    (4) -end end_port_num 
    (5) -w result.json 
    (6) -v True (printing how much time the program has spent)

    Note: Never expect to have users' inputs to be the same as this sequence
    '''

    def __init__(self):
        # print('argv:', argv)
        self.argv_dict = {}
        self.arguments_list = ['-url', '-method', '-start', '-end', '-w', '-v']
        self.write_file = False
        
        for argument in self.arguments_list:
            self.check_input(argument)
            self.allocate_arguments(argument)

        # Translate a host name to IPv4 address
        self.target_ip = socket.gethostbyname(self.argv_dict['-url'])
        self.method = self.argv_dict['-method']
        self.tcp = False
        self.ping = False
        
        for method in self.method:
            if method == 'tcp':
                self.tcp = True
            if method == 'ping':
                self.ping = True
        
        if self.tcp is True:
            self.check_arguments_format()
            self.start_port = self.argv_dict['-start']
            self.end_port =  self.argv_dict['-end']
        
        if self.write_file is True:
            # print('self.argv_dict', self.argv_dict)
            self.result_file_name = self.argv_dict['-w']
        
        if '-v' in argv:
            self.record_time = self.argv_dict['-v']

        print('-'* 50)
        print('The arguments defined by the user:', self.argv_dict)
        print('Scanning host: {}'.format(self.target_ip))
        print('-' * 50)

    def check_input(self, argument):
        if argument in argv:
            next_element = argv[argv.index(argument) + 1]
            if '-' in next_element:
                print('\n Error: no user-defined argument for {}. \n'.format(argument))
                exit()

    def allocate_arguments(self, argument):
        if argument in argv:
            if argument == '-w':
                self.write_file = True
            if argument == '-method':
                self.argv_dict[argument] = []
                next_element = argv[argv.index(argument) + 1]
                next_next_element = argv[argv.index(argument) + 2]
                if '-' not in next_next_element:
                    self.argv_dict[argument].append(next_element)
                    self.argv_dict[argument].append(next_next_element)
                self.argv_dict[argument].append(next_element)
            if argument != '-method':
                self.argv_dict[argument] = argv[argv.index(argument) + 1]

    def check_arguments_format(self):
        if (self.argv_dict['-start'].isdigit() is False) or \
            (self.argv_dict['-end'].isdigit() is False):
            print('\n Error: The provided arguments of -start or -end is/are not valid. \n')
            exit()
        else:
            print('Successfully passed the argument format checks.')

    def tcp_scan(self):

        print('Starting to scan ports of the IP address {} via TCP... \n'.format(self.target_ip))
        
        try:
            open_port_list = []
            close_port_list = []

            self.res_dict = {}

            port_num_range = range(int(self.start_port), int(self.end_port) + 1)

            for port in port_num_range:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                # Ends connection if a port does not respond in 1 second
                result = s.connect_ex((self.target_ip, port))
                # returns an error indicator; open port==0, closed port==1
                if result == 0:
                    print('Port {} is open!'.format(port))
                    open_port_list.append(port)
                    self.res_dict[port] = 'open'
                else:
                    print('Port {} is closed.'.format(port))
                    close_port_list.append(port)
                    self.res_dict[port] = 'closed'
                s.close
            
            if len(open_port_list) != 1:
                print('\nSuccessfully scanned {} ports via TCP. \n{} ports are open,'
                ' {} ports are closed. \n'.format(
                    len(port_num_range), len(open_port_list), len(close_port_list)
                    ))
            else:
                print('\nSuccessfully scanned {} ports via TCP. \n{} port is open,'
                ' {} ports are closed. \n'.format(
                    len(port_num_range), len(open_port_list), len(close_port_list)
                    ))

        except KeyboardInterrupt:
            print('Terminating Scan.')
            exit()

        except socket.gaierror:
            print('Hostname could not be resolved.')
            exit()

    def ping_scan(self):
        print('\n Starting to scan ports of the IP address {} via Ping... \n'.format(self.target_ip))
        result = os.system('ping -c 1 -W 500 {}'.format(self.target_ip)) # 500 毫秒
        self.result_dict = {}
        if result == 0:
            print('\n The connection is active! \n')
            self.result_dict[self.target_ip] = 'open'
        else:
            print('\n The connection is closed. \n')
            self.result_dict[self.target_ip] = 'closed'

    def save_json(self):
        '''
        Format: port_num: open/closed
        '''
        if self.tcp is True:
            with open(self.result_file_name, 'a+') as f:
                content = json.dumps(self.res_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the tcp connection result into a json file {} \n'.format(self.result_file_name))
        
        if self.ping is True:
            ping_file_name = 'ping_' + str(self.result_file_name)
            with open(ping_file_name, 'a+') as f:
                content = json.dumps(self.result_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the ping connection result into a json file {} \n'.format(ping_file_name))


if __name__ == '__main__':
    start_time = time()

    port_scanner = PortScanner()

    if port_scanner.tcp is True:
        port_scanner.tcp_scan()
    if port_scanner.ping is True:
        port_scanner.ping_scan()

    if port_scanner.write_file is True:
        port_scanner.save_json()

    end_time = time()

    if port_scanner.record_time == 'True':
        print('\n The scanning took {} seconds. \n'.format(end_time - start_time))
    
    print('-' * 25 + ' end ' + '-' * 25)

```

test: tcp 

```python
port_scanner_v1.2.py -url www.baidu.com -method tcp -start 20  -end 30  -v False
Successfully passed the argument format checks.
--------------------------------------------------
The arguments defined by the user: {'-url': 'www.baidu.com', '-method': ['tcp'], '-start': '20', '-end': '30', '-v': 'False'}
Scanning host: 104.193.88.77
--------------------------------------------------
Starting to scan ports of the IP address 104.193.88.77 via TCP... 

Port 20 is closed.
Port 21 is closed.
Port 22 is closed.
Port 23 is closed.
Port 24 is closed.
Port 25 is closed.
Port 26 is closed.
Port 27 is closed.
Port 28 is closed.
Port 29 is closed.
Port 30 is closed.
Successfully scanned 11 ports. 0 ports are open, 11 ports are closed.
------------------------- end -------------------------

```

test: ping

```python
python3 port_scanner_v1.2.py -url www.baidu.com -method ping -w ping_result.json  -v True
--------------------------------------------------
The arguments defined by the user: {'-url': 'www.baidu.com', '-method': ['ping'], '-w': 'ping_result.json', '-v': 'True'}
Scanning host: 104.193.88.123
--------------------------------------------------

 Starting to scan ports of the IP address 104.193.88.123 via Ping... 

PING 104.193.88.123 (104.193.88.123): 56 data bytes
64 bytes from 104.193.88.123: icmp_seq=0 ttl=51 time=168.086 ms

--- 104.193.88.123 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 168.086/168.086/168.086/0.000 ms
The connection is active!
Successfully saved the ping connection result into a json file ping_ping_result.json
The scanning took 0.196669340133667 seconds.
------------------------- end -------------------------
```

test: ping + tcp, with all the available parameters

```python

python3 port_scanner_v1.2.py -url www.baidu.com -method tcp ping -start 80 -end 100  -w result.json  -v True
Successfully passed the argument format checks.
--------------------------------------------------
The arguments defined by the user: {'-url': 'www.baidu.com', '-method': ['tcp', 'ping', 'tcp'], '-start': '80', '-end': '100', '-w': 'result.json', '-v': 'True'}
Scanning host: 104.193.88.123
--------------------------------------------------
Starting to scan ports of the IP address 104.193.88.123 via TCP... 

Port 80 is open!
Port 81 is closed.
Port 82 is closed.
Port 83 is closed.
Port 84 is closed.
Port 85 is closed.
Port 86 is closed.
Port 87 is closed.
Port 88 is closed.
Port 89 is closed.
Port 90 is closed.
Port 91 is closed.
Port 92 is closed.
Port 93 is closed.
Port 94 is closed.
Port 95 is closed.
Port 96 is closed.
Port 97 is closed.
Port 98 is closed.
Port 99 is closed.
Port 100 is closed.
Successfully scanned 21 ports via TCP. 
 1 port is open, 20 ports are closed.

 Starting to scan ports of the IP address 104.193.88.123 via Ping... 

PING 104.193.88.123 (104.193.88.123): 56 data bytes
64 bytes from 104.193.88.123: icmp_seq=0 ttl=51 time=168.107 ms

--- 104.193.88.123 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 168.107/168.107/168.107/0.000 ms
The connection is active!
Successfully saved the tcp connection result into a json file result.json
Successfully saved the ping connection result into a json file ping_result.json
The scanning took 10.405949831008911 seconds.
------------------------- end -------------------------

```


## Version 2. Multi Threaded Port Scanner

Reference: [Threaded Port Scanner](https://pythonprogramming.net/python-threaded-port-scanner/?completed=/python-port-scanner-sockets/)

```python
import threading
import time
from queue import Queue
import socket

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.

print_lock = threading.Lock()

target = 'www.baidu.com'
ip = socket.gethostbyname(target)

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # con is the short for connection
        con = s.connect((ip, port))
        with print_lock:
            print('Port', port, 'is open!')
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get() # the worker will get one port number from the queue
        portscan(worker) 
        q.task_done()
        # Queue.task_done lets workers say when a task is done. 
        # Someone waiting for all the work to be done with Queue.join will wait 
        # until enough task_done calls have been made, not when the queue is empty.

q = Queue()

# We are going to create 30 workers as threaders:
for x in range(30):
    # classifying as a daemon, so they will die when the main dies
    t = threading.Thread(target=threader, daemon=True)
    t.start()

# test the first 100 ports
# we can't scan the port no.0 because it is invalid
for worker in range(1, 101):
    q.put(worker) # load the queue with port numbers as each worker

start = time.time()

# wait until the thread terminates.
# Note: If you use .join() and don't call .task_done() for every processed item, 
# your script will hang forever.
q.join()

```

## Version 2.5 Multi Threaded Scanner with Functionality to Input Parameters from the Terminal

1. Added a new parameter: -n as the number of threads

What are the threads going to do: 
* Ping is simple, and not time-consuming, therefore, it is fine with the current single threaded application.
* Tcp socket connecting to the ports is very time-consuming, therefore, we should use multi threading to speed up the efficiency. Note: we should also pay attention to lock: (1) read different ports; (2) write in the json file.

Potential references
* [TCP端口扫描[Python3.5]](https://blog.csdn.net/u014281392/article/details/79237756)
* [使用信号量进行线程同步](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter2/08_Thread_synchronization_with_semaphores.html)
* [Python 3 Multi Threaded Port Scanner](https://rubysash.com/programming/python/python-3-multi-threaded-port-scanner/)

2. Corrected many mistakes and improved the overall clarity of the code.


```python

import os
import json
import socket
import threading
from time import time
from queue import Queue, Empty
from sys import argv, exit

print_lock = threading.Lock()


class PortScanner(object):
    """
    Parameters:
    (1) -url the_web_link
    (2) -method ping/tcp
    (3) -start start_port_num
    (4) -end end_port_num
    (5) -w result.json
    (6) -v True (printing how much time the program has spent)
    (7) -n thread_num
    """

    def __init__(self):
        self.argv_dict = {}
        self.res_dict = {} # for tcp
        self.result_dict = {} # for ping
        self.arguments_list = ['-url', '-method', '-start', '-end', '-w', '-v', '-n']
        self.write_file = False
        self.record_time = None

        for argument in self.arguments_list:
            self.check_input(argument)
            self.allocate_arguments(argument)

        # Translate a host name to IPv4 address
        self.target_ip = socket.gethostbyname(self.argv_dict['-url'])
        self.method = self.argv_dict['-method']
        self.tcp = False
        self.ping = False
        self.thread_number = int(self.argv_dict['-n'])

        for method in self.method:
            if method == 'tcp':
                self.tcp = True
            if method == 'ping':
                self.ping = True

        if self.tcp is True:
            self.check_arguments_format()
            self.start_port = int(self.argv_dict['-start'])
            self.end_port = int(self.argv_dict['-end'])

        if self.write_file is True:
            self.result_file_name = self.argv_dict['-w']

        if '-v' in argv:
            self.record_time = self.argv_dict['-v']

        print('-' * 50)
        print('The arguments defined by the user:', self.argv_dict)
        print('Scanning host: {}'.format(self.target_ip))
        print('-' * 50)

    def check_input(self, argument):
        if argument in argv:
            next_element = argv[argv.index(argument) + 1]
            if '-' in next_element:
                print('\n Error: no user-defined argument for {}. \n'.format(argument))
                exit()

    def allocate_arguments(self, argument):
        if argument in argv:
            if argument == '-w':
                self.write_file = True
            if argument == '-method':
                self.argv_dict[argument] = []
                next_element = argv[argv.index(argument) + 1]
                # To avoid the error when users input -method ping/tcp as the last argu
                if argv.index(next_element) != (len(argv) - 1):
                    next_next_element = argv[argv.index(argument) + 2]
                    if '-' not in next_next_element:
                        self.argv_dict[argument].append(next_element)
                        self.argv_dict[argument].append(next_next_element)

                self.argv_dict[argument].append(next_element)
            if argument != '-method':
                self.argv_dict[argument] = argv[argv.index(argument) + 1]

    def check_arguments_format(self):
        if (self.argv_dict['-start'].isdigit() is False) or \
                (self.argv_dict['-end'].isdigit() is False):
            print('\nError: The provided arguments of -start or -end is/are not valid.\n')
            exit()
        else:
            print('Successfully passed the argument format checks.')

    def threader(self):
        while True:
            try:
                # the worker will get one port number from the queue
                port = self.q.get(block=True, timeout=1)
                self.scan(port)
                self.q.task_done()
            except Empty:
                break
    
    def scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        # Ends connection if a port does not respond in 1 second
        result = s.connect_ex((self.target_ip, port))
        # returns an error indicator; open port==0, closed port==1
        try:
            print_lock.acquire()
            if result == 0:
                print('Port {} is open!'.format(port))
                self.open_port_list.append(port)
                self.res_dict[port] = 'open'
            else:
                print('Port {} is closed.'.format(port))
                self.close_port_list.append(port)
                self.res_dict[port] = 'closed'
        finally:
            print_lock.release()
            s.close()

    def tcp_scan(self):

        print('\nStarting to scan ports of the IP'
              ' address {} via TCP... \n'.format(self.target_ip))

        self.open_port_list = []
        self.close_port_list = []

        port_num_range = range(self.start_port, self.end_port)

        self.q = Queue()
        thread_list = []

        for port in port_num_range:
            self.q.put(port)

        for _ in range(self.thread_number):
            t = threading.Thread(target=self.threader)
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

        if len(self.open_port_list) != 1:
            print('\nSuccessfully scanned {} ports via TCP. \n{} ports are open,'
                  ' {} ports are closed. \n'.format(len(port_num_range),
                                                    len(self.open_port_list),
                                                    len(self.close_port_list))
                  )
        else:
            print('\nSuccessfully scanned {} ports via TCP. \n{} port is open,'
                  ' {} ports are closed. \n'.format(len(port_num_range),
                                                    len(self.open_port_list),
                                                    len(self.close_port_list))
                  )

    def ping_scan(self):
        print('\n Starting to scan ports of the IP'
              ' address {} via Ping... \n'.format(self.target_ip))
        result = os.system('ping -c 1 -W 500 {}'.format(self.target_ip))  # 500 毫秒

        if result == 0:
            print('\n The connection is active! \n')
            self.result_dict[self.target_ip] = 'open'
        else:
            print('\n The connection is closed. \n')
            self.result_dict[self.target_ip] = 'closed'

    def save_json(self):
        """
        Format: port_num: open/closed
        """
        if self.tcp is True:
            with open(self.result_file_name, 'a+') as f:
                content = json.dumps(self.res_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the tcp connection'
                  ' result into a json file {} \n'.format(self.result_file_name))

        if self.ping is True:
            ping_file_name = 'ping_' + str(self.result_file_name)
            with open(ping_file_name, 'a+') as f:
                content = json.dumps(self.result_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the ping connection'
                  ' result into a json file {} \n'.format(ping_file_name))

def main():
    start_time = time()
    port_scanner = PortScanner()

    if port_scanner.tcp is True:
        port_scanner.tcp_scan()
    if port_scanner.ping is True:
        port_scanner.ping_scan()
    if port_scanner.write_file is True:
        port_scanner.save_json()

    end_time = time()
    if port_scanner.record_time == 'True':
        print('\n The scanning took {} seconds. \n'.format(end_time - start_time))
    print('-' * 25 + ' end ' + '-' * 25)


if __name__ == '__main__':
    main()

```

test

```python
assignment1.py -url www.baidu.com -method tcp ping -v True -w result.json -n 30 -start 30 -end 100
Successfully passed the argument format checks.
--------------------------------------------------
The arguments defined by the user: {'-url': 'www.baidu.com', '-method': ['tcp', 'ping', 'tcp'], '-start': '30', '-end': '100', '-w': 'result.json', '-v': 'True', '-n': '30'}
Scanning host: 104.193.88.77
--------------------------------------------------

Starting to scan ports of the IP address 104.193.88.77 via TCP... 

Port 30 is closed.
Port 40 is closed.
Port 31 is closed.
Port 37 is closed.
Port 36 is closed.
Port 35 is closed.
Port 38 is closed.
Port 39 is closed.
Port 33 is closed.
Port 32 is closed.
Port 34 is closed.
Port 41 is closed.
Port 42 is closed.
Port 44 is closed.
Port 43 is closed.
Port 50 is closed.
Port 47 is closed.
Port 46 is closed.
Port 45 is closed.
Port 48 is closed.
Port 49 is closed.
Port 54 is closed.
Port 53 is closed.
Port 58 is closed.
Port 56 is closed.
Port 57 is closed.
Port 55 is closed.
Port 59 is closed.
Port 51 is closed.
Port 52 is closed.
Port 80 is open!
Port 60 is closed.
Port 69 is closed.
Port 62 is closed.
Port 63 is closed.
Port 70 is closed.
Port 71 is closed.
Port 66 is closed.
Port 61 is closed.
Port 64 is closed.
Port 65 is closed.
Port 68 is closed.
Port 85 is closed.
Port 72 is closed.
Port 73 is closed.
Port 78 is closed.
Port 67 is closed.
Port 75 is closed.
Port 77 is closed.
Port 76 is closed.
Port 81 is closed.
Port 79 is closed.
Port 83 is closed.
Port 84 is closed.
Port 82 is closed.
Port 87 is closed.
Port 86 is closed.
Port 89 is closed.
Port 74 is closed.
Port 88 is closed.
Port 90 is closed.
Port 91 is closed.
Port 92 is closed.
Port 95 is closed.
Port 93 is closed.
Port 94 is closed.
Port 97 is closed.
Port 96 is closed.
Port 99 is closed.
Port 98 is closed.

Successfully scanned 70 ports via TCP. 
1 port is open, 69 ports are closed. 


 Starting to scan ports of the IP address 104.193.88.77 via Ping... 

PING 104.193.88.77 (104.193.88.77): 56 data bytes
64 bytes from 104.193.88.77: icmp_seq=0 ttl=51 time=170.484 ms

--- 104.193.88.77 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 170.484/170.484/170.484/0.000 ms

 The connection is active! 


 Successfully saved the tcp connection result into a json file result.json 


 Successfully saved the ping connection result into a json file ping_result.json 


 The scanning took 2.7327497005462646 seconds. 

------------------------- end -------------------------
```