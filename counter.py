from collections import Counter

list = ["A", "A", "B", "C"]
# for v in list:
#     print(v, list.count(v))

#for v in set(list):
#    print(v, list.count(v))

count_value = Counter(list)

print(count_value.most_common())
print(count_value)