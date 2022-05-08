import numpy as np
import copy

class museum_state():                                       #初始化博物馆
    def __init__(self,shape):
        self.m,self.n = shape                               #博物馆的大小m，n
        self.robotsroom = np.zeros((self.m,self.n))         #博物馆房间:0:m-1,0:n-1，有守卫时值置为1
        #遍历点坐标，遍历点坐标范围：1:m，1:n
        self.x = 0
        self.y = 0
        self.robotnum = 0                                       #放置的机器人数

def setrobot(oldmuseum,x,y):                #放机器人的函数，x，y为遍历点，移动范围：0:m-1，0:n-1
    museum = copy.deepcopy(oldmuseum)       #返回个新的博物馆
    museum.robotnum+=1                      #放的机器人+1
    museum.robotsroom[x,y] = 1              #机器人位置设1
    tag = 1                                 #tag为1则被监控
    #放完机器人后，向右移动遍历点至未被监控房间，当博物馆房间都被监控时，遍历点会停在[m,1]
    while(museum.x<= museum.m-1 and tag!=0):
        museum.y+=1
        if(museum.y>museum.n-1):            #说明要换行了
            museum.x += 1
            museum.y = 0
        if(museum.x!=museum.m):
            tag = jugle(museum)             #判断该房间是否被监控
    return museum

#判断遍历点是否被监控,检查自己上中下左右是否有机器人存在
def jugle(museum):
    tag = 0                                 #0未被监控
    positions = [[0, 0],
                 [0,-1],
                 [0, 1],
                 [-1,0],
                 [1, 0],
                 ]
    #处理边界情况太复杂，这里我们新建个临时房间数组：0:m+1,0:n+1，给机器人房间外面围一圈值为0的边界
    temproom = np.zeros([museum.m+2,museum.n+2])
    temproom[1:museum.m+1,1:museum.n+1] = museum.robotsroom
    temp_x = museum.x+1                     #博物馆的位置范围0:m-1对应临时房间数组的1:m
    temp_y = museum.y+1
    #检查上中下左右房间
    for i in range(5):
        pos_x = temp_x+positions[i][0]
        pos_y = temp_y+positions[i][1]
        if(temproom[pos_x,pos_y] == 1):
            tag = 1
    return tag

def juglegoal(museum):                      #判断这个房间是否到终点
    Tag = 0
    if(museum.x==museum.m):
        Tag = 1
    return Tag

def main():
    # f = open('input.txt')
    # txt = []
    # for line in f:
    #     txt.append(line.strip())
    # m = int(txt[0])
    # n = int(txt[1])
    m = 7
    n = 6
    minrobots = m*n/2#最少机器人数
    robotsposition = np.zeros([m,n])    #存机器人摆放方案
    i= 0
    museum = museum_state([m,n])        #初始化一个博物馆并放入队列
    museum_list = []
    museum_list.append(museum)
    
    while(museum_list):
        museum_tmp = museum_list.pop(0)#广度优先算法
        # museum_tmp = museum_list.pop()#深度优先算法
        goal = juglegoal(museum_tmp)
        if (not goal):#当未遍历到最终点时
            if museum_tmp.x<m-1:#放下面，当x不是最下面那行就可以放下面
                newmuseum = setrobot(museum_tmp,museum_tmp.x+1,museum_tmp.y)
                if newmuseum.robotnum<=minrobots:
                    museum_list.append(newmuseum)
            if museum_tmp.y<n-1:#放右边
                newmuseum = setrobot(museum_tmp,museum_tmp.x,museum_tmp.y+1)
                if newmuseum.robotnum <= minrobots:
                    museum_list.append(newmuseum)
            if (True):#放自己
                newmuseum = setrobot(museum_tmp, museum_tmp.x, museum_tmp.y )
                if newmuseum.robotnum <= minrobots:
                    museum_list.append(newmuseum)

        else:#遍历点到终点了
            i+=1
            if museum_tmp.robotnum<=minrobots:
                minrobots = museum_tmp.robotnum
                robotsposition = museum_tmp.robotsroom

    with open(r".\output.txt", "w") as op:
        op.write(str(minrobots))
        op.write('\n')
        op.write(str(robotsposition))
        op.close()
    print(minrobots,'\n',robotsposition)


if __name__ == "__main__":
    main()