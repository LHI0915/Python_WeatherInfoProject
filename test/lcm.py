from gcd import gcd

def lcd(a, b):
    g = gcd(a, b)
    x, y = a // g, b // g
    print("함수 lcd 실행")
    return x * y * g

if __name__ == '__main__':
    x, y = [int(n) for n in input("두 수를 입력하세요:").split()[:2]]
    l = lcd(x, y)
    print("%d와 %d의 최소 공배수는 %d 입니다." % (x, y, l))
    print("lcd 실행")