words = {}
def read_file(file_address = 'teste'):
	with open(file_address, encoding='utf-8') as f:
		line = f.read()
		for word in line.split():
			try:
				words[word] += 1
			except:
				words[word] = 1

read_file()
print(words)