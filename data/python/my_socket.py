# server
import socket
import select

PORT = ...

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = PORT                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print "Listening on port {p}...".format(p=port)

s.listen(5)                 # Now wait for client connection.
while True:
    try:
        client, addr = s.accept()
        ready = select.select([client,],[], [],2)
        if ready[0]:
            data = client.recv(4096)
            print data
    except KeyboardInterrupt:
        print
        print "Stop."
        break
    except socket.error, msg:
        print "Socket error! %s" % msg
        break

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# client
try:
    # sending them separately
    for e in elems:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        client.connect((host, PORT))
        client.send(e)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
except Exception as msg:
    print ms
