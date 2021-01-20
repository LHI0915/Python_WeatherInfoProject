
# 두 수를 입력받아 최대공약수를 구한다. 

def gcd(a, b):
    if a < b:
        a, b = b, a
    if a % b == 0:
        return b
    print("함수 gcd 실행")
    return gcd(b, a % b)


if __name__ == '__main__':
    x, y = [int(n) for n in input("두 수를 입력하세요:").split()[:2]]
    g = gcd(x, y)
    print("%d와 %d의 최대 공약수는 %d 입니다." % (x, y, g))
    print("gcd 실행")