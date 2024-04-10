import random
import string


SAMPLEE = string.ascii_letters + string.digits + string.punctuation

def get_random_combination(length=12):
    '''
    获得一个由数字, 字母, 标点符号随即构成的密钥.
    '''
    return ''.join(random.sample(SAMPLEE, length))


if __name__ == '__main__':
    for i in range(10):
        print(get_random_combination())