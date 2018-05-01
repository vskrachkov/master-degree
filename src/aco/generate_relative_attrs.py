import csv
import collections
import random

f = open('results.csv', 'w')

main_list = [
    f'Верстат {i}' for i in range(1, 20 + 1)
]
dq = collections.deque(main_list)
w = csv.writer(f, delimiter=',')

for i in main_list:
    dq.popleft()
    for j in dq:
        w.writerow((
            i, j, round(random.randint(500, 1700) * 0.01, 2)
        ))

f.close()
