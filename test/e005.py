from lcm import lcd
from functools import reduce

def main():
    n = reduce(lcd, range(1, 21))
    print(n)

if __name__ == '__main__':
    main()