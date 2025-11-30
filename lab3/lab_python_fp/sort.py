data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    result = sorted(data)
    result.reverse()
    print(result)

    result_with_lambda = sorted(data, key=lambda x: -x)
    print(result_with_lambda)