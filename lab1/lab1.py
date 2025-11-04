import sys

def get_coef(index):
    try:
        N = sys.argv[index]
    except(BaseException):
        N = input('Введите ' + chr(64+index) + ':\n')

    while True:
        try:
            N = float(N)
            break
        except(BaseException):
            print("Введено не действительное число")
            N = input('Введите ' + chr(65 + index) + ':\n')

    return N

def Bi2_equation(A, B, C):
    result = []
    Dis = B**2 - A*C*4
    if Dis > 0:
        result.append((-B - (Dis ** 2)) / (2 * A))
        result.append((-B + (Dis ** 2)) / (2 * A))
    elif Dis == 0:
        result.append(-B / (2 * A))
    return result

def main():
    A = get_coef(1)
    B = get_coef(2)
    C = get_coef(3)
    res = Bi2_equation(A, B, C)
    if len(res) == 2:
        print(f"Корни: {res[0]} и {res[1]}")
    elif len(res) == 1:
        print(f"Корень: {res[0]}")
    else:
        print("Нет корней")

main()