col,row = 3,3
T = [[0 for _ in range(col)] for _ in range(row)]
for i in range(col):
    for j in range(row):
        T[i][j] = (i-1,j)
print(T)