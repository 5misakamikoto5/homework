import numpy as np
import copy

class museum_state():#初始化博物馆
    def __init__(self,shape):
        self.m,self.n = shape                               #博物馆的m，n
        self.robotsroom = np.zeros((self.m,self.n))         #机器人房间:0:m-1,0:n-1
        self.room_supervise = np.zeros((self.m+2,self.n+2))     #被监控的位置：1:m,1:n;总空间大小：1:m+1,1:n+1

        #遍历点坐标，遍历点坐标范围：1:m，1:n
        self.x = 1
        self.y = 1

        self.robotnum = 0                                       #放置的机器人数
        self.roomnum = 0                                        #监控的房间数

        #给博物馆受监控的房间围一层，处理边界情况
        for i in range(self.m+2):
            self.room_supervise[i,0] = 1
            self.room_supervise[i,self.n+1] = 1
        for j in range(self.n+2):
            self.room_supervise[0,j] = 1
            self.room_supervise[self.m+1,j] = 1

def setrobot(oldmuseum,x,y):                #放机器人的函数，xy为遍历点在roomsupervise范围内移动：1:m，1:n
    positions = [[0, 0],
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]]
    museum = copy.deepcopy(oldmuseum)#返回个新的博物馆
    museum.robotnum+=1#放的机器人+1
    museum.robotsroom[x-1,y-1] = 1#机器人位置设1

    #设置受监督的房间
    for i in range(5):
        pos_x = x + positions[i][0]
        pos_y = y + positions[i][1]
        museum.room_supervise[pos_x,pos_y]+=1
        if(museum.room_supervise[pos_x,pos_y]==1):              #等于1的时候说明是新被监控的房间
            museum.roomnum+=1

    #向右移动遍历点
    while(museum.x<= museum.m and museum.room_supervise[museum.x,museum.y]!=0):
        museum.y+=1
        if(museum.y>museum.n):#说明要换行了
            museum.x+=1
            museum.y = 1
    return museum

def main():
    m,n = 4,4
    minrobots = m*n#最少机器人数
    robotsposition = np.zeros([m,n])#存机器人摆放方案
    i= 0

    museum = museum_state([m,n])
    museum_list = []
    museum_list.append(museum)

    while(museum_list):
        museum_tmp = museum_list.pop(0)
        if (museum_tmp.roomnum<m*n):#当监控的房间数小于总房间数
            #感觉这里有问题的放置策略
            if museum_tmp.x<m:#放下面，当x不是最下面那行就可以放下面
                newmuseum = setrobot(museum_tmp,museum_tmp.x+1,museum_tmp.y)
                if newmuseum.robotnum<=minrobots:
                    museum_list.append(newmuseum)
            if (museum_tmp.y < n):  # 放右边
                newmuseum = setrobot(newmuseum, museum_tmp.x, museum_tmp.y + 1)
                if newmuseum.robotnum <= minrobots:
                    museum_list.append(newmuseum)
            if (True):#放自己
                newmuseum = setrobot(museum_tmp,museum_tmp.x,museum_tmp.y)
                if newmuseum.robotnum <= minrobots:
                    museum_list.append(newmuseum)

        elif(museum_tmp.roomnum>=m*n):#监控房间数满了
            i+=1
            if museum_tmp.robotnum<=minrobots:
                minrobots = museum_tmp.robotnum
                robotsposition = museum_tmp.robotsroom

    with open(r".\test2.txt", "w") as op:
        op.write(str(minrobots))
        op.write('\n')
        op.write(str(robotsposition))
        op.close()
    print(minrobots,'\n',robotsposition,'\n',i)


if __name__ == "__main__":
    main()