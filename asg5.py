import csv
import random

digits = {i:[] for i in range(0,10)}
IMAGE_SIZE = 64
noise_domain = [i for i in range(-3, 4)]
htrans_domain = [0, 1, 2]
vtrans_domain = [-1, 0, 1]

def read_digits_from(file_name = 'teste'):
    line = None
    with open(file_name) as digits_file:
        digits_content = csv.DictReader(digits_file)
        for row in digits_content:
            for index, value in row.items():
                digits[int(index)].append(int(value))

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


def simplegen(digits, noise):
    raw_pixels = generate_values_for('noise_domain', noise)
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

def transformgen(digits, noise, htrans, vtrans):
    htrans_values = generate_values_for('htrans_domain', htrans)
    vtrans_values = generate_values_for('vtrans_domain', vtrans)
    pass

def main():
    read_digits_from('assignments/asg/code/digits/digits.csv')
    # random.seed()
    noise = [0.0025, 0.0125, 0.0350, 0.9000, 0.0350, 0.0125, 0.0025]
    obs = simplegen(digits, noise)
    print(simplerec(obs, digits, noise))



if __name__ == '__main__':
    main()
