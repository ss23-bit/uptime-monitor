def digitize(n):
    result = []

    for digit in str(n):
        result.insert(0, int(digit))

    return result

n = 35789

print(digitize(n))