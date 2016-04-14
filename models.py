import csv
import random

digits = {i:[] for i in range(0,10)}
IMAGE_SIZE = 64
noise_domain = [i for i in range(-3, 4)]
htrans_domain = [0, 1, 2]
vtrans_domain = [-1, 0, 1]

def read_digits_from(file_name = ''):
    """
    Read a csv file and write it to a digits variable. The given csv
    MUST have the first row as the labels.

    Args:
        file_name (String): The file to be read (local or full path from this directory).
    """
    with open(file_name) as digits_file:
        digits_content = csv.DictReader(digits_file)
        for row in digits_content:
            for index, value in row.items():
                digits[int(index)].append(int(value))

def read_same_digit_from(file_name = '', digit = 0):
    with open(file_name) as digits_file:
        digits_content = csv.reader(digits_file)
        for row in digits_content:
            for value in row:
                digits[digit].append(int(value))


def generate_values_for(type_of_domain, distribution):
    values = []
    for position in range(len(distribution)):
        amount = round(distribution[position] * IMAGE_SIZE)
        for i in range(amount):
            values.append(globals()[type_of_domain][position])
    return values #make this random!


def calc_prob_oij(pixel, noise, obs_pixel):
    raw = pixel + noise
    if (obs_pixel == raw) or \
            (obs_pixel == 1 and raw < 1) or \
            (obs_pixel == 4 and raw > 4):
        return 1.0
    else:
        return 0.0


def simplegen(digits, noise, choice = -1):
    """
    Generate a transformed digit based on the given noise

    Args:
        digits (dict): The dictionary that contains the possible digits
            and their signature (digit : [digit_signature]).
        noise (array): The noise distribution.

    Returns:
        array: Digit signature from noisy digit.
    """
    raw_pixels = generate_values_for('noise_domain', noise)
    if choice < 0:
        random.seed()
        choice = random.randint(0, 9)
    for i in range(IMAGE_SIZE):
        raw_pixels[i] += digits[choice][i]
        if(raw_pixels[i] > 4):
            raw_pixels[i] = 4
        elif(raw_pixels[i] < 1):
            raw_pixels[i] = 1
    return raw_pixels

def simplerec(obs, digits, noise):
    """
    Calculate the conditional probabilities of an observed digit to be a 
    digit from 1 to 0. The observed digit is noisy.

    Args:
        obs (array): The observed digit
        digits (dict): The dictionary that contains the possible digits
            and their signature. digit : [digit_signature]
        noise (array): The distribution of the noise.

    Returns:
        dict: Dictionary containing the conditional probabilities for 
            digits from 1 to 0.
    """
    probs = {}
    sum_probs = 0
    noise_values = generate_values_for('noise_domain', noise)
    for key in digits.keys():
        prob_d = 1/10 # uniform distribution for the keys
        product = 1.0
        for position in range(IMAGE_SIZE):
            prob_nj = 0.0
            prob_oij = calc_prob_oij(digits[key][position], 
                noise_values[position], obs[position])
            for prob_noise in noise:
                prob_nj += (prob_noise * prob_oij)
            product *= prob_nj
        probs[key] = prob_d * product
        sum_probs += probs[key]
    
    for i in range(len(probs)):
        probs[i] = probs[i]/sum_probs
    return probs

def new_index(base, trans_value, difference):
    return base + round(trans_value * (5 - difference)/4)

def transformgen(digits, noise, htrans, vtrans):
    """
    Generate a transformed digit based on the given noise and transformation
    distribution.

    Args:
        digits (dict): The dictionary that contains the possible digits
            and their signature (digit : [digit_signature]).
        noise (array): The noise distribution.
        htrans (array): The horizontal transformation distribution
        vtrans (array): The vertical transformation distribution

    Returns:
        array: Digit signature from transformed digit.
    """
    htrans_values = generate_values_for('htrans_domain', htrans)
    vtrans_values = generate_values_for('vtrans_domain', vtrans)
    random.seed()
    choice = random.randint(0, 9)
    warped = {choice: []}
    for i in range(8):
        for j in range(8):
            pos = i * 8 + j
            v = new_index(i, vtrans_values[pos], j)
            h = new_index(j, htrans_values[pos], i)
            try: 
                new_pos = v * 8 + h
                warped[choice].append(digits[choice][new_pos])
            except:
                warped[choice].append(1)
    return simplegen(warped, noise, choice)

def transformrec(obs, digits, noise, htrans, vtrans):
    """
    Calculate the conditional probabilities of an observed digit to be a 
    digit from 1 to 0. The observed digit is noisy and transformed.

    Args:
        obs (array): The observed digit
        digits (dict): The dictionary that contains the possible digits
            and their signature. digit : [digit_signature]
        noise (array): The distribution of the noise.
        htrans (array): The distribution of the horizontal transformation
        vtrans (array): The distribution of the vertical transformation

    Returns:
        dict: Dictionary containing the conditional probabilities for 
            digits from 1 to 0.
    """
    probs = {}
    sum_probs = 0
    noise_values = generate_values_for('noise_domain', noise)
    htrans_values = generate_values_for('htrans_domain', htrans)
    vtrans_values = generate_values_for('vtrans_domain', vtrans)
    for key in digits.keys():
        sum_h = 0
        for prob_h in htrans:
            sum_v = 0
            for prob_v in vtrans:
                prod_i = 1
                for i in range(8):
                    prod_j = 1
                    for j in range(8):
                        sum_nij = 0
                        for prob_noise in noise:
                            pos = i * 8 + j
                            v = new_index(i, vtrans_values[pos], j)
                            h = new_index(j, htrans_values[pos], i)
                            new_pos = v * 8 + h
                            try:
                                digit_pixel = digits[key][new_pos]
                            except:
                                digit_pixel = 1
                            prob_oij = calc_prob_oij(digit_pixel, 
                                noise_values[pos], obs[pos])
                            sum_nij += (prob_noise * prob_oij)
                        prod_j *= sum_nij
                    prod_i *= prod_j
                sum_v += (prod_i * prob_v)
            sum_h += (sum_v * prob_h)
        probs[key] = 1/10 * sum_h
        sum_probs += probs[key]

    for i in range(len(probs)):
        probs[i] = probs[i]/sum_probs
    return probs    

class Classifier():
    """
    This Classifier uses Naive Bayes to classify the given data
    """
    def __init__(self):
        """
        Initialize frequency considering 10 digits (0..9) and four shades possible
        in each pixel (1..4)
        """
        self.frequency = {}
        for digit in range(0, 10):
            shades = {shade:0 for shade in range(1, 5)}
            self.frequency[digit] = shades
        self.total = 0

    def train(self, data, labels):
        """
        Train the classifier with the given digits and their labels

        Args:
            data (array of arrays): A t*n size matrix with the training data
            labels (array): A t size array with the labels
        """
        for label in range(len(labels)):
            for pixel in data[label]:
                self.frequency[label][pixel] += 1
                self.total += 1



    def test(self, data):
        """
        Receive a matrix with the testing set.
        I know this is wrong. I tried to use Naive Bayes and couldn't make it work
        proberly.

        Args:
            data (array of arrays): A m*n size matrix with the training data

        Returns:
            array: m size array containing the classification of each given digit
        """
        labels = []
        for row in data:
            frequency = {shade:0 for shade in range(1, 5)}
            total = 0
            for pixel in row:
                frequency[pixel] += 1
                total += 1

            label = -1
            max_diff = 1000
            print(frequency)
            for digit, distribution in self.frequency.items():
                probability_train = 1
                probability_test = 1
                for shade, value in distribution.items():
                    probability_train *= (value/self.total)
                    probability_test *= (frequency[shade]/total)
                diff = abs(probability_train - probability_test)
                print(probability_train, probability_test)
                if diff < max_diff:
                    label = digit
                    max_diff = diff
            labels.append(label)
        return labels        


def main():
    classifier = Classifier()
    data = []
    labels = []
    path = 'assignments/asg/code/digits/digit.{}.csv'
    for i in range(10):
        path2 = path.format(i)
        read_same_digit_from(path2, i)
    for label, digit in digits.items():
        data.append(digit)
        labels.append(label)
    classifier.train(data, labels)

    path = 'assignments/asg/code/digits/digits.csv'
    global digits
    digits = {i:[] for i in range(0,10)}
    read_digits_from(path)
    test = []
    for label, digit in digits.items():
        test.append(digit)
        labels.append(label)
    print(digits)
    print(classifier.test(test))

    
    # print(classifier.frequency)
    # print(classifier.total)
    # random.seed()
    # noise = [0.0025, 0.0125, 0.0350, 0.9000, 0.0350, 0.0125, 0.0025]
    # obs = simplegen(digits, noise)
    # htrans = [0.5625, 0.2500, 0.1875]
    # vtrans = [0.2500, 0.5625, 0.1875]

    # obs = transformgen(digits, noise, htrans, vtrans)
    # print(transformrec(obs, digits, noise, htrans, vtrans))

if __name__ == '__main__':
    main()
