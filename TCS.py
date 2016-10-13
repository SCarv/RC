#!/usr/bin/python3

from nlsocket import * 
from argparse import ArgumentParser

class TCS:

	TRSdict = { # TODO example only
		'French' : ('rodrigo', 59001),
		'English': ('tomas'  , 59002),
		'Spanish': ('rafael' , 59003),
	}

	sock = nlsocket(AF_INET, SOCK_DGRAM) # Must be DGRAM!
	addr = None

	def __init__(self, port): 
		self.addr = (gethostname(), port) 
		self.sock.bind(self.addr)
		
	def sendULR(self, client, args):
		'''
		Sends "ULR N L1 L2 L3 ... Ln" through the socket.
		'''
		lang_count = str(len(self.TRSdict))
		langs = ' '.join(self.TRSdict)
		msg = 'ULR ' + lang_count + ' ' +  langs
		print('Sending:\n' + msg + '\n...to:', client)
		msg = msg.encode()
		self.sock.nlsendto(msg, client)
		print('Message sent')

	def unr(self, client, args):
		'''
		 Sends "UNR IP PORT" through the socket.
		'''
		language = args[0]
		TRS = self.TRSdict[language]
		msg = 'UNR ' + TRS[0] + ' ' + str(TRS[1])
		print('Sending message [', msg, '] to', client)
		msg = msg.encode()
		self.sock.nlsendto(msg, client)
		print('Message sent')

	def parse_recv(self, msg):	
		(req, args) = msg.split(maxsplit=1)
		args = args.split()

	def wait_for_msg(self):
		print('Waiting for a request...')
		(msg, client) = self.sock.nlrecvfrom()
		print('Got message', msg, 'from', client)

		
	def TCSloop(self):
		''' Loops forever listening for a message on the socket,
		and then executing the command asked for in that message'''
		print('Welcome to the TCS! Hosted on', self.addr)
		while 1:
			self.wait_for_msg()
			msg = msg.decode()
			cmd = msg[0:3]
			args = msg[3:].split()
			if cmd == 'ULQ':
				self.ulr(client, args)
			elif cmd == 'UNQ':
				self.unr(client, args)
			else:
				print('Malformed message!')
		
def sendULR(sock, client):
	pass
def sendUNR(sock, client):
	pass
def sendSUR(sock, client):
	pass

def parseULQ(ulq):
	return ulq == b'ULQ\n'

def parseUNQ(unq):
	'''
	Returns the requested language.
	'''
	sp = unq.split(b' ')
	if sp[0] == b'UNQ' and len(sp) == 2  and ulr.endswith(b'\n'): 
		return sp[1].encode()
	else:
		return None

def parseSRG(srg):
	'''Returns the new TRS in {language: (addr, port)} form'''
	sp = unq.split(b' ')
	if len(sp) == 4 and sp[0] == b'SRG' and srg.endswith(b'\n')
	and sp[3].isdigit():
		return {sp[1].decode(): (sp[2].decode(), sp[3])}

def parseSUN():
	pass
		
def parse_port():                                                               
    ''' Returns the port number on which this server will run.''' 
    ap = ArgumentParser() 
    ap.add_argument('-p', '--port', type=int, 
	help='Port number on which this server will run.')
    opts = ap.parse_args()
    return opts.port if opts.port else 58051

def main():
	port = parse_port()
	tcs = TCS(port)
	tcs.TCSloop()

if __name__ == '__main__': main()
