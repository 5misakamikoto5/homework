import numpy as np

def mintraj(matrix):
    col,row = matrix.shape
    dp = np.zeros((col,row))                                #dp数组
    min_id = [[0 for _ in range(col)] for _ in range(row)]  #列表，记录达到本点的最短路径的上一个点
    traj = []                                               #存储最短路径

    # dp updatad
    dp[0,0] = matrix[0,0]                                   #首先更新dp[0,0]
    for i in range(1,col):                                  #更新dp[:,0]和dp[0,:]
        dp[i,0] = dp[i-1,0] + matrix[i, 0]
        min_id[i][0] = [i-1, 0]                             #更新记录上一个点的列表
    for j in range(1,row):
        dp[0,j] = dp[0,j-1] + matrix[0,j]
        min_id[0][j] = [0, j-1]
    for i in range(1,col):                                  #由于只能向右，向下移动，对于dp[i,j],只需比较左边和上边的点的大小即可
        for j in range(1,row):
            dp[i,j] = min(dp[i-1,j]+matrix[i,j],dp[i,j-1]+matrix[i,j])
            if dp[i-1,j]<=dp[i,j-1]:                        #根据左边和上边的点大小比较，记录下上一个点的坐标
                min_id[i][j] = [i-1,j]
            else:
                min_id[i][j] = [i,j-1]

    mint = dp[col-1,row-1]                                  #最短路径记录在dp[col-1,row-1]中
    id = [col-1,row-1]                                      #根据最后的点坐标，从min_id中一直查找上一个点坐标直到结束
    traj.append([col-1,row-1])
    while(id!=[0,0]):
         id = min_id[id[0]][id[1]]
         traj.append(id)
    traj.reverse()
    return mint,traj

def main():
    matrix = np.random.randint(0,15,(5,5))
    mint,traj = mintraj(matrix)
    print("最短路径长度：",mint,'\n',
          "最短路径：",traj,'\n',
          "原矩阵:",'\n',matrix)

if __name__ == '__main__':
    main()

