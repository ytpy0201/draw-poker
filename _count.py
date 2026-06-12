from collections import Counter

my_list = ["A", "A", "B", "C"]
counts = Counter(my_list)

for v, count in counts.items():
    print(v, count)