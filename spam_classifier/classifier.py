import codecs
import os

words = {'sex': 0, 'watch': 0, 'viagra': 0, 'free': 0,
    'money': 0, 'single': 0, 'love': 0, 'women': 0,
    'looking': 0, 'investment': 0, 'fast': 0,
    'cash': 0, 'ad': 0, 'boss':0, 'score': 0,
    'order': 0, 'buy': 0, 'income':0, 'price': 0,
    'employment': 0, 'bargain': 0, 'cost': 0, 'save': 0,
    'profit': 0, 'friend': 0, 'hello': 0, 'dear': 0,
    'click': 0, 'unsubscribe': 0, 'marketing': 0,
    'notspam': 0, 'satisfied': 0, 'giving': 0,
    'win': 0, 'won': 0, 'winner': 0, 'winning': 0,
    'rolex': 0, 'rolex': 0}


def write_attributes_description():
    with open('training.arff', 'w') as arff:
        arff.write("@relation DATA=spam-filter\n\n")
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

def read_folder(folder = 'spam/TRAINING/', training = True):
    if training:
        file_label = {}
        with open('spam/SPAMTrain.label', 'r') as labels:
            for line  in labels:
                classifier = line.split()
                file_label[ classifier[1] ] = classifier[0]
        for name, label in file_label.items():
            read_file(folder + name, label)
    else:
        files = os.listdir(folder)
        for f in files:
            read_file(folder + f)

write_attributes_description()
read_folder()
