import random


def ticket():
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    a = ''
    for i in range(30):
        a += random.choice(s)
    return a


