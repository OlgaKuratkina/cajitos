def multipliers():
    return [lambda x: x * i for i in range(3)]

print(multipliers())
print([m(5) for m in multipliers()])
