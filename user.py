#!/usr/bin/python3

from nlsocket import *
from argparse import ArgumentParser
from cmd import Cmd

class Client(Cmd):

	intro = "Welcome to the RC translation client. Type 'help'!"
	prompt = '(RC) '
	TCSsock = nlsocket(AF_INET, SOCK_DGRAM)  
	TCSaddr = ()
	TRSsock = nlsocket(AF_INET, SOCK_STREAM)
	languages = []
	
	def __init__(self, TCSaddr):
		super().__init__() # call superclass's constructor
		self.TCSaddr = TCSaddr

	def do_list(self, argv):
		'Query a list of all avaliable languages.'
		sendULQ()
		langs = recvULR()
		for i in range(len(languages)):
			print(i,'>', languages[i])
		self.languages = languages

	def do_request(self, args):
		'Request to connect to a particular TRS.'
		sendUNQ(lang)
		TRSaddr = recvUNR()
		TRSsock.connect(TRSaddr)
		sendTRS(sock)
		recvTRR(sock)	

	def do_exit(self, argv):
		'Close the program.'
		self.TCSsocket.close()
		if self.TRS: TRS.close()
		raise SystemExit
	
	def do_EOF(self, argv):
		'Close the program.'
		print()
		self.do_exit(argv)

def sendULQ(sock, client):
	sock.nlsendto(b'ULQ\n', client)	

def sendUNQ(sock, client):

def sendTRQ(sock, client):

def parseULR(ulr):
	'''
	Returns all avaliable languages in a list.
	'''
	sp = ulr.split(b' ')
	langc = sp[0:1]
	langs = sp[1:]
	#TODO maybe: check each individual word for length
	return sp[0] == b'ULR' and ulr.endswith(b'\n') and
		langc.isdigit() and int(langc) == len(langs) 

def parseUNR(unr):
	'''
	Returns the requested TRS in (addr, port) form.
	'''
	sp = unr.split(b' ')
	if sp[0] == b'UNR' and len(sp) == 3 and ulr.endswith(b'\n')
	and sp[2].isdigit():
		return (sp[1].decode(), int(sp[2]))
	else:
		return None

def recvTRR(socket):
	if recv_word(3) == b'TRR':
		2nd = recv_word(3)
		if 2nd == 't':
			return recvTRQtext()
		if 2nd == 'f':
			return recvTRQfile()
		if 2nd == 'ERR':
			return 'ERR'
		if 2nd == 'NTA':
			return 'NTA'
	else:
		return None

	def recvTRQfile():
		filename = recv_word(100)
		size     = recv_word(10)
		try: 
			content  = recv(int(size))
			return ('f', filename.decode(), content)
		except ValueError: 
			return None
				
	def recvTRQtext():
		langs = ()
		N = recv_word(2)
		if not N.isidigit():
			return None
		for _ in range(int(N)):
			langs += recv_word(LANG_LEN)
		if not recv(1) == b'\n':
			return None
		return langs

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
