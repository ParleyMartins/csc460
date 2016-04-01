import codecs
import os

words = {'sex': 0, 'watch': 0, 'viagra': 0, 'free': 0,
	'money': 0, 'single': 0, 'love': 0, 'women': 0,
	'looking': 0, 'investment': 0, 'fast': 0,
	'cash': 0}


def write_attributes_description():
	with open('training.arff', 'w') as arff:
		for word in words.keys():
			arff.write("@attribute {} numeric\n".format(word))
		arff.write("@attribute class {0, 1}\n")
		arff.write("\n@data\n")

def write_attributes_values(label):
	with open('training.arff', 'a') as arff:
		for word, value in words.items():
			arff.write("{},".format(value))
			words[word] = 0
		arff.write("{}\n".format(label))


def read_file(file_address = 'TRAIN_00000.eml', label = 0):
	with codecs.open(file_address, encoding='quopri') as f:
		line = f.read()
		for word in line.split():
			word = word.lower()
			try:
				word = word.decode('utf-8')
				words[word] += 1
			except:
				pass
		write_attributes_values(label)

def read_folder(folder = 'spam/TRAINING/'):
	file_label = {}
	with open('spam/SPAMTrain.label', 'r') as labels:
		for line  in labels:
			classifier = line.split()
			file_label[ classifier[1] ] = classifier[0]
	for name, label in file_label.items():
		read_file(folder + name, label)

write_attributes_description()
read_folder()
