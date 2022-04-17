
from queue import Queue
import random
from tokenize import String
from tracemalloc import start
from typing import List

class P:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
        
def init():
    board = list()
    with open('test3.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            board.append(line.strip())
    return board 

def findPos(t,x): 
    result = list()

    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == x: result.append(P(i,j))
    return result

def drawPath(n):
    path = ''
    for i in range(n):
        path = path + (random.sample(['L','R','U','D'], 1)[0])
    return path 

def setPosition(board,path,Ps):
    def moveP(p,move):
        if move=='U': newP = P(p.x-1,p.y)
        if move=='D': newP = P(p.x+1,p.y)
        if move=='L': newP = P(p.x,p.y-1)
        if move=='R': newP = P(p.x,p.y+1)

        if (not (0<=newP.x and newP.x<len(board))) or (not (0<=newP.y and newP.y<len(board[0]))):
            return p 
        if board[newP.x][newP.y]=='#': return p
        return newP

    newPs = list()
    for p in Ps:
        for move in path:
             p = moveP(p,move)
        newPs.append(p)
    return newPs

class State:
    def __init__(self,ps,sciezka):
        '''
        ps ->      lista pozycji gdzie moze znajdować się komandos po przeyciu ścieżki
        ścieżka -> string 
        '''

        self.ps, self.sciezka = ps, sciezka
    def __str__(self):
        return f"({self.ps} ; {self.sciezka})"
    def __repr__(self):
        return f"({self.ps} ; {self.sciezka})"

def BFS(board,startPs,endPs,initialPath):
    # MXPATH = s
    Q = Queue() 
    visited = dict()

    def addToQueue(state,path):
        if not str(state) in visited:
            visited[str(state)] = True
            Q.put(State(state,path))

    def check(ps):
        for p in ps:
            czyjestp = False
            for e in endPs:
                if (p.x==e.x and p.y==e.y): czyjestp = True
            if czyjestp==False: return False
        return True 

    def movePs(ps,move):
        newPs = list()
        for p in ps:
            if move=='U': newP = P(p.x-1,p.y)
            if move=='D': newP = P(p.x+1,p.y)
            if move=='L': newP = P(p.x,p.y-1)
            if move=='R': newP = P(p.x,p.y+1)

            if (not (0<=newP.x and newP.x<len(board))) or (not (0<=newP.y and newP.y<len(board[0]))): newP = p 
            if board[newP.x][newP.y]=='#': newP = p 
            newPs.append(newP)
        return newPs
    
    addToQueue(startPs,initialPath)

    while not Q.empty():
        state = Q.get()
        ps, path = state.ps, state.sciezka

        print(f"ps = {ps}, path = {path}")
        
        if len(path)>MXPATH: continue
        if check(ps): return path

        psL, pathL = movePs(ps,'L') , path + 'L'
        addToQueue(psL,pathL)

        psR, pathR = movePs(ps,'R'), path + 'R'
        addToQueue(psR,pathR)

        psU, pathU = movePs(ps,'U'), path + 'U'
        addToQueue(psU,pathU)

        psD, pathD = movePs(ps,'D'), path + 'D'
        addToQueue(psD,pathD)

def solve():
    board = init()
    startPos, endPos = findPos(board,'S'), findPos(board,'G')
    # print(f'startPos = {startPos}')
    startPos = startPos + findPos(board,'B')
    # print(f'startPos = {startPos}')
    endPos = endPos + findPos(board,'B')

    # for d in range((len(board)-2)//2, len(board)-2):
    initialPath = drawPath(0)
    ps = setPosition(board,initialPath,startPos)

    result = BFS(board,ps,endPos,initialPath)
    if not result==False:
        return result

    return False


def run():

    print(solve())


    # with open( 'zad_output.txt', 'w' ) as file:
    #     # result = solve()
    #     # if result == False: result = "False"
    #     # print(result)
    #     file.write(''.join(solve()))

run()
    
