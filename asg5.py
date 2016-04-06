import csv
import random

digits = {i:[] for i in range(0,10)}
IMAGE_SIZE = 64
noise_domain = [i for i in range(-3, 4)]

def read_digits_from(file_name = 'teste'):
    line = None
    with open(file_name) as digits_file:
        digits_content = csv.DictReader(digits_file)
        for row in digits_content:
            for index, value in row.items():
                digits[int(index)].append(int(value))

def generate_noise(distribution):
    noise_values = []
    for position in range(len(distribution)):
        amount = round(distribution[position] * IMAGE_SIZE)
        for i in range(amount):
            noise_values.append(noise_domain[position])
    return noise_values

def calc_prob_oij(pixel, noise, obs_pixel):
    raw = pixel + noise
    if (obs_pixel == raw) or \
        (obs_pixel == 1 and raw < 1) or \
        (obs_pixel == 4 and raw > 4):
        return 1
    else:
        return 0


def simplegen(digits, noise):
    raw_pixels = generate_noise(noise)
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
    noise_values = generate_noise(noise)
    for key in digits.keys():
        prob_d = 1/10 # uniform distribution for the keys
        product = 1
        for position in range(IMAGE_SIZE):
            prob_nj = 0
            prob_oij = calc_prob_oij(digits[key][position], 
                noise_values[position], obs[position])
            for prob_noise in noise:
                prob_nj += prob_noise*prob_oij
            product *= prob_nj
        probs[key] = prob_d * product
    print(probs)
    return probs

def main():
    read_digits_from('assignments/asg/code/digits/digits.csv')
    # random.seed()
    noise = [0.0025, 0.0125, 0.0350, 0.9000, 0.0350, 0.0125, 0.0025]
    obs = simplegen(digits, noise)
    simplerec(obs, digits, noise)



if __name__ == '__main__':
    main()
