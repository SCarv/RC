def get_word_trans(lang_file, word):
	lang_file.seek(0) # restart read pointer to beginning
	for line in lang_file.readlines():
		(estrg, tuga) = line.split()
		if tuga == word:
			return estrg
	return None # if no such image is avaliable
		
def get_image_trans_filename(img_file, filename):
	'''
	Returns the filename corresponding to the translation image.
	Returns None if no such translation exists.
	'''
	img_file.seek(0) # restart read pointer to beginning
	for line in img_file.readlines():
		(estrgf, tugaf) = line.split(' ', 1)
		if tugaf == filename:
			return estrgf
	return None # if no such image is avaliable

def TRSloop(listener):
	while 1:
		(server, clientaddr) = listener.accept()
		msg = recvTRQ(listener)
			if type(msg == file)
			# TODO check for file or word translation	

def sendTRR(sock):
	pass

def sendSUN(sock, client):
	pass

def parseSRR():
	sp = unq.split(b' ')
	if len(sp) == 2 and sp[0] == b'SRR' and 
	(sp[1] == b'ERR' or sp[1] == b'OK' or sp[1] == b'ERR') and
	srg.endswith(b'\n'):
		return sp[1].decode()

def parseSUR():
	return NotImplemented #TODO

def recvTRQ(sock):
	if sock.recv(4) == b'TRQ ':
		2nd = sock.recv(1)
		if 2nd == 't':
			return recvTRRtext()
		elif 2nd == 'f':
			return recvTRRfile()
		elif 2nd == 'E' and sock.recv(2) == b'RR':
			return 'ERR'
		elif 2nd == 'N' and sock.recv(2) == b'TA':
			return 'NTA'
	return None

	def recvTRQfile():
		filename = b''
		while not filename.endswith(b' '):
			filename += sock.recv(1)
		size = b''
		while not size.endswith(b' '):
			size += sock.recv(1)
		content  = recv(int(size))
		return ('f', filename.decode(), content)
				
	def recvTRQtext():
		words = ()
		N = recv_word(3)
		if not N.isidigit():
			return None
		for _ in range(int(N)):
			words.append(recv_word(LANG_LEN))
		if not recv(1) == b'\n':
			return None
		return words

def main():
	listener = nlsocket(AF_INET, SOCK_STREAM)
	listener.listen(BACKLOG)
	TRSloop(listener)
