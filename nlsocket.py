_buffersize = 512

def nlrecv(sock):
    '''
    Does multiple recvs until it finds a newline.
    '''    
    msg = b''
    while not msg.endswith(b'\n'):
        msg += sock.recv(_buffersize)
    return msg
    
def nlrecvfrom(sock):
    '''
    Same as normal recvfrom, but only stops reading when it finds a newline.
    Does not take a '_buffersize' argument since it only stops at the newline.
    '''
    (msg, addr) = sock.recvfrom(_buffersize)
    while not msg.endswith(b'\n'):
        msg += sock.recv(_buffersize)
    return (msg, addr)

def nlsend(sock, msg):
    if not msg.endswith(b'\n'):
        msg += b'\n'
    sentc = 0
    print('Waiting for', addr, 'to receive', msg, '... ', end='')
    while sentc < len(msg):
        sentc += sock.send(msg[sentc:])
    print('Done.')
    return sentc

def nlsendto(sock, msg, addr):
    if not msg.endswith(b'\n'):
        msg += b'\n'
    sentc = 0
    print('Waiting for', addr, 'to receive', msg, '... ', end='')
    while sentc < len(msg):
        sentc += sock.sendto(msg[sentc:], addr)
    print('Done.')
    return sentc

