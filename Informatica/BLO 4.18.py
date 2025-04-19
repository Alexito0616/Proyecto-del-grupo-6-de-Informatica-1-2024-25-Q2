v = [1,2,3,2,1]
i = 0
j = len(v)

while i < len(v) and j != 0:
    i = i + 1
    j = j - 1

if v[i] == v[j]:
    print("SI")

else:
    print("NO")
