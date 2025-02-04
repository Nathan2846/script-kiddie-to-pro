import sys 
import socket
import threading

"""
This is a boolean short-circuit technique
For each int 0-255, if the length of the corresponding hex character is 3 (human readable)
then append that character to the filter. Otherwise get a dot
Then, concat all that into a string
"""
HEX_FILTER= ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    if isinstance (src,bytes):
        src=src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        #Translate the raw string into english using the filter where possible
        printable = word.translate(HEX_FILTER)

        # Translate the raw string to hex
        hexa = ' '.join(f'{ord(c):02X}' for c in word)
        hexwidth = length*3

        # Hold the output
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results

def receive_from(connection):
    """
    Read the data into the buffer until there is no more data
    or an error occurs
    """
    buffer = b''

    connection.settimeout(5)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass

    return buffer

def request_handler(buffer):
    # Perform packet modifications
    return buffer

def response_handler(buffer):
    #Perform packet modifications
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    #receive first and dump if needed
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    #Send to localhost
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print('[<==] Sending %d bytes to localhost' % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True: #Begin main loop
        #Recieve from client 
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>]Receieved %d bytes from localhost." % len(local_buffer)
            print (line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer) #Modify
            remote_socket.send(local_buffer) #Send along
            print ('[==>]Sent to remote')
        
        remote_buffer = receive_from(remote_socket) #Get data back
        if len(remote_buffer):
            print ('[<==]Receieved %d bytes from remote.' % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer) #Modify
            client_socket.send(remote_buffer) #Send on its way to locahost

            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer): #If one end stops talking, close the connection
            client_socket.close()
            remote_socket.close()
            print('[*] No more data. Closing connections')
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print ('Problem on bind: %r' % e)
        print ('[!!] Failed to listen on %s:%d' % (local_host, local_port))
        print ('[!!] Check for other listening sockets or correct permissions (try tuning with sudo!)')
        sys.exit(0)

    print('Listening on %s:%d' % (local_host, local_port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        #Print local connection info
        line = '> Received incoming connection from %s:%d' % (addr[0], addr[1])
        print(line)

        #Start a thread for this remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print('Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receieve_first]')
        print ('Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True')
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if "true" in receive_first.lower():
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()