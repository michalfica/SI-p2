from queue import Queue
import random
from tokenize import String
from tracemalloc import start
from turtle import pos
from typing import List

class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, P):
            return (self.x==other.x and self.y==other.y)
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is NotImplemented:
            return NotImplemented
        return not x

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
        
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

def drawPath(board):
    path =''.join(   ['L']*len(board[0]) + ['D']*len(board) + ['R']*len(board[0]) + ['U']*len(board))
    return path 

def setPosition(board,path,Ps):
    def moveP(p,move):
        newP = P(p.x,p.y) 

        """
            ^-- tu mogą być kłopoty
        """

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

def BFS(board,startPs,endPs,initialPath,DEBUG=False):
    MAXPATHLEN = 150 
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
        return set(newPs)
    
    addToQueue(startPs,initialPath)

    while not Q.empty():
        state = Q.get()
        ps, path = state.ps, state.sciezka
        
        if DEBUG:
            print(f"ps = {ps}, path = {path}")

        if len(path) > MAXPATHLEN: continue
        if check(ps): return path

        psL, pathL = movePs(ps,'L') , path + 'L'
        addToQueue(psL,pathL)

        psR, pathR = movePs(ps,'R'), path + 'R'
        addToQueue(psR,pathR)

        psU, pathU = movePs(ps,'U'), path + 'U'
        addToQueue(psU,pathU)

        psD, pathD = movePs(ps,'D'), path + 'D'
        addToQueue(psD,pathD)
    return False

def solve(DEBUG=False):
    board = init()
    startPos, endPos = findPos(board,'S'), findPos(board,'G')
    startPos = startPos + findPos(board,'B')
    endPos = endPos + findPos(board,'B')

    if DEBUG:
        print(f"startpos = {startPos}")

    initialPath = drawPath(board)
    ps = setPosition(board,initialPath,startPos)

    if DEBUG:
        print(f"initial path: {initialPath}")
        print(f"ps = {ps}")

    if not DEBUG:

        result = BFS(board,ps,endPos,initialPath,DEBUG)
        if not result==False:
            return result

    return "NIE ZNALAZŁEM\n"


def run():
    with open( 'zad_output.txt', 'w' ) as file:
        file.write(''.join(solve(False)))

run()
    
