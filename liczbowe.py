l = []

n = 3
# i = 3

# for _ in range(i):
for x in range(1, n+1):
    for y in range(1, n+1):
        for z in range(1, n+1):
            # for a in range(1, n+1):
                l.append(x+y+z)#+a)

for value in range(3, 3*n+1):
    print(f'Dla x={value} -> y={l.count(value)}')
