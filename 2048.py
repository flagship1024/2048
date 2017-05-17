
# coding:UTF-8
import random
import sys
import os
v = [[0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0]]
'''
    显示界面  
'''
def display(v,score):
#    print '{0:4}'.format(0)
    print ("{0:4} {1:4} {2:4} {3:4}".format(v[0][0], v[0][1], v[0][2], v[0][3]))
    print ('{0:4} {1:4} {2:4} {3:4}'.format(v[1][0], v[1][1], v[1][2], v[1][3]))
    print ('{0:4} {1:4} {2:4} {3:4}'.format(v[2][0], v[2][1], v[2][2], v[2][3]))
    print ('{0:4} {1:4} {2:4} {3:4}'.format(v[3][0], v[3][1], v[3][2], v[3][3]))       

    print ('total score: ',score)

# 初始化二维矩阵，每一行各个元素以1/2,1/3,1/6的概率随机填入0,2,4
# v[0]:[2, 2, 2, 4]
# v[1]:[2, 2, 0, 0]
# v[2]:[2, 2, 0, 2]
# v[3]:[2, 0, 0, 2]

def init(v):
    for i in range(4):
        v[i] = [random.choice([0,0,0,2,2,4])for x in range(4)]
        print ("v[%s]:%s"%(i,v[i]))

# 对齐非零的数字  
# direction == 'left'：向左对齐，例如[8,0,0,2]左对齐后[8,2,0,0]  
# direction == 'right'：向右对齐，例如[8,0,0,2]右对齐后[0,0,8,2]  
# remove() 函数用于移除列表中某个值的第一个匹配项。
# Input：W(Up) S(Down) A(Left) D(Right) Q(Quit), press <CR>.
#    0    0    0    4
#    0    0    0    2
#    2    2    0    2
#    2    0    2    0
# ************LEFT****************************
# ------------row1------------------
# zeros:[0]
# zeros:[0]
# zeros:[0]
# alignList:[4, 0, 0, 0]
# ------------row2------------------
# zeros:[0]
# zeros:[0]
# zeros:[0]
# alignList:[2, 0, 0, 0]
# -----------row3-------------------
# zeros:[0]
# alignList:[2, 2, 2, 0]
# zeros:[0]
# zeros:[0]
# alignList:[4, 2, 0, 0]
# -----------row4-------------------
# zeros:[0]
# zeros:[0]
# alignList:[2, 2, 0, 0]
# zeros:[0]
# zeros:[0]
# zeros:[0]
# alignList:[4, 0, 0, 0]

def align(vList,direction):
    for i in range(vList.count(0)):
        vList.remove(0)
        zeros = [0 for x in range(4 - len(vList))]
        print ("zeros:%s"%(zeros))

        if direction == 'left':
            vList.extend(zeros)
        else:
            vList.insert(0,zeros)
    print ("alignList:%s"%(vList))


# 在列表查找相同且相邻的数字相加, 找到符合条件的返回True，否则返回False,同时还返回增加的分数  
# direction == 'left':从右向左查找，找到相同且相邻的两个数字，左侧数字翻倍，右侧数字置0  
# direction == 'right':从左向右查找，找到相同且相邻的两个数字，右侧数字翻倍，左侧数字置0 

def addsame(vList,direction):
    score = 0
    if direction == 'left':
        for i in [0,1,2]:
            if vList[i] == vList[i+1] != 0:
                vList[i] *= 2
                vList[i+1] = 0
                score = score + vList[i]
                return {'bool':True , 'score':score}
    else:
        for i in [3,2,1]:
            if vList[i] == vList[i-1] != 0:
                vList[i] *=2
                vList[i-1] = 0
                score = score + vList[i]
                return {'bool':True ,'score':score}
    return {'bool':False,'score':score}


# 处理一行（列）中的数据--排整齐，得到最终的该行（列）的数字状态值, 返回得分  
# vList: 列表结构，存储了一行（列）中的数据  
# direction: 移动方向,向上和向左都使用方向'left'，向右和向下都使用'right'  
  
def handle(vList,direction):
    print ("-"*30)
    totalScore = 0
    align(vList,direction)
    result = addsame(vList,direction)
    while result['bool'] == True:
        totalScore += result['score']
        align(vList,direction)
        result = addsame(vList,direction)
    return totalScore


# 根据移动方向重新计算矩阵状态值，并记录得分
# ------------------A/a-------------------
# 0    4    4    0      8    0    0    0  
# 0    0    0    0  >>  0    0    0    0
# 2    2    2    2      8    0    2    0
# 0    2    2    0      4    0    0    0

def operation(v):
    totalScore = 0
    # 初始化游戏标志位和方向信息，为False时表示游戏结束
    gameOver = False
    direction = 'left'

    op = input('operater:')
    
    if op in ['A','a']:
        direction = 'left'
        for row in range(4):
            # print ("v[%s]=%s"%(row,v[row]))
            totalScore += handle(v[row],direction)

    elif op in ['D','d']:
        direction = 'right'
        for row in range(4):
            totalScore += handle(v[row],direction)
    elif op in ['W','w']:
        direction = 'up'
        for col in range(4):
            #将每列的值复制成新的列表进行处理
            vList = [v[row][col] for row in range(4)]
            totalScore += handle(vList,direction)
            #将处理后的值覆盖原矩阵中的值
            for row in range(4):
                v[row][col] = vList[row]
    elif op in ['S','s']:
        direction = 'down'
        for col in range(4):
            #将每列的值复制成新的列表进行处理
            vList = [v[row][col] for row in range(4)]
            totalScore += handle(vList,direction)
            #将处理后的值覆盖原矩阵中的值
            for row in range(4):
                v[row][col] = vList[row]
    elif op in ['Q','q']:
        print ("Are you sure Quit Game?")
        exit(0)               
    else:
        print ("Invalid input, please enter a charactor in [W, S, A, D] or the lower")
        return {'gameOver':gameOver,'score':totalScore}
    # 统计空白区域数目N
    N = 0
    for q in v:
        N += q.count(0)
    if N == 0:
        gameOver = True
        return {'gameOver':gameOver,'score':totalScore}
    # 按2和4出现的几率为3/1来产生随机数2和4
    num = random.choice([2,2,2,4])
    # 产生随机数k，上一步产生的2或4将被填到第k个空白区域
    k = random.randrange(1,N+1)
    n = 0
    for i in range(4):
        for j in range(4):
            if v[i][j] == 0:
                n += 1
                if n == k:
                    v[i][j] = num
                    break
    return {'gameOver':gameOver,'score':totalScore}

if __name__ == "__main__":
    init(v)
    score = 0
    print ('Input：W(Up) S(Down) A(Left) D(Right) Q(Quit), press <CR>.')
    while True:
        # 呈现矩阵结果，及分数
        display(v,score)
        result = operation(v)
        if result['gameOver'] == True:
            print ('Game Over,You fail!!!')
            print ('Your total score:',score)
        else:
            score += result['score']
            if score >= 2048:
                print ('Game Over,You Win!!!')
                print ('Your total score:%s'%(score))