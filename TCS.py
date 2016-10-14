#!/usr/bin/python3

from socket import * 
from nlsocket import * 
from argparse import ArgumentParser
from collections import OrderedDict
		
def TCSloop(servsock):
	''' Loops forever listening for a message on the socket,
	and then executing the command asked for in that message'''

	print('Welcome to the TCS! Hosted on', servsock.getsockname())

	TRSdict = OrderedDict()

	while 1:
		print('Now waiting for messages.')
		(msg, clientaddr) = nlrecvfrom(servsock)
		print('Received', msg, 'from', clientaddr)

		if parseULQ(msg) != None:
			sendULR(servsock, clientaddr, list(TRSdict))
			continue

		lang = parseUNQ(msg)	
		if lang != None:
			try: TRSaddr = TRSdict[lang]
			except KeyError: TRSaddr = None
			sendUNR(servsock, clientaddr, TRSaddr)
			continue

		TRS = parseSUN(msg)	
		if TRS != None:
			status = True if TRS[2] == clientaddr else False
			sendSUR(servsock, TRSaddr, status)
			continue	

		TRS = parseSRG(msg)	
		if TRS != None:
			TRSdict.update(TRS)
			sendSRR(servsock, clientaddr)
			continue

		print('Malformed message')
		
def sendULR(clientSock, clientAddr, langs):
	ulr = 'ULR ' + str(len(langs)) + ' ' + ' '.join(langs) + '\n'
	ulr = ulr.encode()
	nlsendto(clientSock, ulr, clientAddr)

def sendUNR(clientSock, clientAddr, TRSaddr):
	(name, port) = TRSaddr
	unr = 'UNR ' + name + ' ' + str(port) + '\n'
	unr = unr.encode()
	nlsendto(clientSock, unr, clientAddr)
	
def sendSUR(TRSsock, TRSaddr, good):
	status = b'OK' if good else b'NOK'
	sur = 'SUR ' + good + '\n'
	sur = sur.encode()
	nlsendto(TRSsock, unr, TRSaddr)

def parseULQ(ulq):
	if ulq == b'ULQ\n': 
		return True

def parseUNQ(unq):
	'''
	Returns the requested language.
	'''
	sp = unq.split(b' ')
	if len(sp) == 2 and sp[0] == b'UNQ' and unq.endswith(b'\n'): 
		return sp[1].encode()

def parseSRG(srg):
	'''Returns the new TRS in {language: (addr, port)} form'''
	sp = srg.split(b' ')
	if len(sp) == 4 and sp[0] == b'SRG' and sp[3].isdecimal() and srg.endswith(b'\n'):
		return {sp[1].decode(): (sp[2].decode(), int(sp[3]))}

def parseSUN(sun):
	sp = sun.split(b' ')
	if len(sp) == 4 and sp[0] == b'SUN' and sp[3].isdigit():
		return {sp[1].decode(): (sp[2].decode(), int(sp[3]))}
		
def parse_port():                                                               
    ''' Returns the port number on which this server will run.''' 
    ap = ArgumentParser() 
    ap.add_argument('-p', '--port', type=int, 
	help='Port number on which this server will run.')
    opts = ap.parse_args()
    return opts.port if opts.port else 58051

def main():
	port = parse_port()
	serv = socket(AF_INET, SOCK_DGRAM)
	serv.bind((gethostname(), port))
	TCSloop(serv)

if __name__ == '__main__': main()
