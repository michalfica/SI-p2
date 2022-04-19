from queue import Queue
from queue import PriorityQueue
from tokenize import String
from typing import List
from xmlrpc.client import MAXINT

from numpy import result_type

class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __eq__(self, other):
        if isinstance(other, P):
            return (self.x==other.x and self.y==other.y)
        return NotImplemented

    def __ne__(self, other):
        x = self.__eq__(other)
        if x is NotImplemented:
            return NotImplemented
        return not x

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def dist(self,other):
        return abs(self.x-other.x) + abs(self.y-other.y)
        
def init():
    board = list()
    with open('zad_input.txt', 'r') as file:
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

def setPosition(board,path,Ps):
    def moveP(p,move):
        newP = P(p.x,p.y) 

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
    return set(newPs)

class State:
    def __init__(self,ps,g,h,sciezka):
        '''
        ps ->      lista pozycji gdzie moze znajdować się komandos po przeyciu ścieżki
        ścieżka -> string 
        '''

        self.ps, self.sciezka = ps, sciezka
        self.g, self.h = g, h
    def __str__(self):
        return f"({self.ps} ; {self.sciezka})"
    def __repr__(self):
        return f"({self.ps} ; {self.sciezka})"

def BFS(board,startPs,endPs,initialPath):
    MAXPATHLEN = 150 
    Q = PriorityQueue()
    visited = dict()

    def addToQueue(state,g,h,path):
        if not str(state) in visited:
            visited[str(state)] = True
            Q.put((g+h,State(state,g,h,path)))

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

            if board[newP.x][newP.y]=='#': newP = p 
            newPs.append(newP)
        return set(newPs)

    def h(ps):
        """
        zwraca max z odległości do najbliżśzego punktu docelowego dla każdej pozycji w stanie 
        """
        result = 0
        for p in ps:
            result = max( result, min( [p.dist(e) for e in endPs]) )
        return result 

    numberOfPs = len(startPs)
    addToQueue(startPs,0,h(startPs),initialPath)

    while not Q.empty():
        state = Q.get()[1]
        ps, g, path = state.ps, state.g, state.sciezka

        if len(path) > MAXPATHLEN or len(ps) > numberOfPs: continue
        if check(ps): return path

        if len(ps) < numberOfPs:
            numberOfPs = len(ps)

        psL, pathL = movePs(ps,'L') , path + 'L'
        hL = h(psL)
        addToQueue(psL,g+1,hL,pathL)

        psR, pathR = movePs(ps,'R'), path + 'R'
        hR = h(psR)
        addToQueue(psR,g+1,hR,pathR)

        psU, pathU = movePs(ps,'U'), path + 'U'
        hU = h(psU)
        addToQueue(psU,g+1,hU,pathU)

        psD, pathD = movePs(ps,'D'), path + 'D'
        hD = h(psD)
        addToQueue(psD,g+1,hD,pathD)
    return False

def solve():
    board = init()
    startPos, endPos = findPos(board,'S'), findPos(board,'G')
    startPos = startPos + findPos(board,'B')
    endPos = endPos + findPos(board,'B')

    initialPath = ''
    ps = setPosition(board,initialPath,startPos)

    result = BFS(board,ps,endPos,initialPath)
    if not result==False:
        return result

    return "NIE ZNALAZŁEM\n"

def run():
    with open( 'zad_output.txt', 'w' ) as file:
        file.write(''.join(solve()))

run()
    
