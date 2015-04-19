s=None
# For a server which returns (0,1) depending on how we modify the ciphertexts

def connect():
    import socket; global s
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try: s.connect(('54.165.60.84',80))
    except socket.error as e: print e; return -1
    print "Connected to server!"; return 0

def disconnect():
    if not s: 'Not connected!'; return 0
    s.close(); print "Connection closed!"; return 0

# Packet Structure: < num_blocks(1) || ciphertext(16*num_blocks) || null-terminator(1) >

def send(ctext,blocks):
    if not s: return -1
    msg=ctext[:]; msg.insert(0,blocks); msg.append(0)
    s.send(bytearray(msg)); recvbit=s.recv(2)
    try: return int(recvbit)
    except ValueError as e: return int(recvbit[0])
