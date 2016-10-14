#!/usr/bin/python3

from nlsocket import *
from socket import *
from argparse import ArgumentParser
import cmd

class Client(cmd.Cmd):

    intro = "Welcome to the RC translation client. Type 'help'!"
    prompt = '(RC) '
    TCSsock = socket(AF_INET, SOCK_DGRAM)
    TRSsock = socket(AF_INET, SOCK_STREAM)
    TCSaddr = None
    
    def __init__(self, TCSaddr):
        super().__init__() # call superclass's constructor
        self.TCSaddr = TCSaddr

    def do_list(self, argv):
        'Query a list of all avaliable languages.'
        sendULQ(self.TCSsock, self.TCSaddr)
        langs = recvULR(self.TCSsock)
        for i in range(len(langs)):
            print(i,'>', langs[i])

    def do_request(self, args):
        'Request to connect to a particular TRS.'
        request(lang)
        args = args.split()
        try:
            langn = int(args[0])
            tf = args[1]
            words = args[2:]
        except (ValueError, IndexError):
            print('Malformed input.')
        else:
            sendUNQ(langn, tf, words)
            TRSaddr = recvUNR(self.TCSaddr)
            self.TRSsock.connect(TRSaddr)
            sendTRQ(TRSsock)
            wors = recvTRR(TRSsock)    

    def do_exit(self, argv):
        'Close the program.'
        self.TCSsocket.close()
        if self.TRS: TRS.close()
        raise SystemExit
    
    def do_EOF(self, argv):
        'Close the program.'
        print()
        self.do_exit(argv)

	

def sendULQ(TCSsock, TCSaddr):
    nlsendto(TCSsock, b'ULQ\n',TCSaddr)

def sendUNQ(TCSsock, TCSaddr, langn):
    unq = 'UNQ ' + language + '\n'
    unq = unq.encode()
    nlsendto(TCSsock, unq, TCSaddr)

def sendTRQ(TRSsock, img_filename):
    '''Sends "TRS f filename size data\n'''
    with open(img_filename, 'rb') as img:
        contents = img.read()
        trq = b'TRQ ' + b'f ' + img_filename.encode() + b' ' + bytes([len(contents)]) + contents + b'\n'
        sentc = 0
        while sentc != len(msg):
            sentc += TRSsock.send(trq)

def recvULR(TCSsock):
    '''
        Gets ULR message and checks if it is in form "ULR
        Returns all avaliable languages in list form.
    '''
    ulr = nlrecv(TCSsock)
    sp = ulr.split(b' ')
    try:
        langc = sp[1]
        langs = sp[2:]
    except IndexError:
        return
    #TODO maybe: check each individual word for length
    if sp[0] == b'ULR' and ulr.endswith(b'\n') and langc.isdigit() and int(langc) == len(langs):
        return langs

def recvUNR(TCSsock):
    '''
    Returns the requested TRS in (addr, port) form.
    '''
    unr = nlrecv(self.TCSsocket, 400)
    sp = unr.split(b' ')
    if sp[0] == b'UNR' and len(sp) == 3 and ulr.endswith(b'\n') and sp[2].isdigit():
        return (sp[1].decode(), int(sp[2]))

def recvTRR(TRSsock):
        if TRSsock.recv(4) == b'TRQ ':
                opt = TRSsock.recv(1)
                if opt == 't':
                        return recvTRRtext()
                elif opt == 'f':
                        return recvTRRfile()
                elif opt == 'E' and TRSsock.recv(2) == b'RR':
                        return 'ERR'
                elif opt == 'N' and TRSsock.recv(2) == b'TA':
                        return 'NTA'
        return None

        def recvTRQfile():
            filename = b''
            while not filename.endswith(b' '):
                filename += TRSsock.recv(1)

            size = b''
            while not size.endswith(b' '):
                size += TRSsock.recv(1)

            content  = recv(int(size))
            return ('f', filename.decode(), content)
                
        def recvTRQtext():
            N = TRSsock.recv(2)
    
            words = b''
            for _ in range(int(N)):
                words += TCSTRSsock.recv(1)
                while not word.endswith(' '):
                    words += TCSTRSsock.recv(1)
    
            if TRSsock.recv(1) == b'\n':
                return words.split()

def parseTCSaddr():
    ''' Returns the name and the port number of the TCS server.'''
    ap = ArgumentParser()
    ap.add_argument('-p', '--port', type=int,
        help='Port number of the listening TCS server.')
    ap.add_argument('-n', '--name', type=str,
        help='Host name of the listening TCS server.')
    opts = ap.parse_args()
    name = opts.name if opts.name else gethostname()
    port = opts.port if opts.port else 58051
    return (name, port)

def main():
    TCSaddr = parseTCSaddr()
    client = Client(TCSaddr)
    client.cmdloop()

if __name__ == '__main__': main()
