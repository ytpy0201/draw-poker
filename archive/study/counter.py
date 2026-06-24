from collections import Counter

list = ["A", "C", "B", "C"]
# for v in list:
#    print(v, list.count(v))

#for v in set(list):
#    print(v, list.count(v))

count_value = Counter(list)

print(count_value)

#(要素, 出現回数)というタプルを出現回数順に並べたリストを返す
#print(count_value.most_common())
