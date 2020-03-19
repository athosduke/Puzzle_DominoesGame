import math
import random
import time
from queue import PriorityQueue
import copy

def solve_distinct_disks(length, n):
    if length<=n:
        return None
    #create board
    board = []
    goalboard = []
    for i in range (1,length+1):
        if i <= n:
            board.append(i)
        else:
            board.append(0)
        if i > length-n:
            goalboard.append(length-i+1)
        else:
            goalboard.append(0)
            
    def disk_successors(board):
        for i in range(length):
            if board[i]!=0:
                if i >= 1:
                    if i>=2:
                        if board[i-1]>0 and board[i-2]==0:
                            newboard = copy.copy(board)
                            newboard[i-2]=newboard[i]
                            newboard[i]=0
                            yield i,i-2,newboard
                    if board[i-1]==0:
                        newboard = copy.copy(board)
                        newboard[i-1]=newboard[i]
                        newboard[i]=0
                        yield i,i-1,newboard
                if i <= length-2:
                    if i<= length-3:
                        if board[i+1]>0 and board[i+2]==0:
                            newboard = copy.copy(board)
                            newboard[i+2]=newboard[i]
                            newboard[i]=0
                            yield i,i+2,newboard
                    if board[i+1]==0:
                        newboard = copy.copy(board)
                        newboard[i+1]=newboard[i]
                        newboard[i]=0
                        yield i,i+1,newboard

    def disk_h(board):
        count = 0
        for i in range(length):
            if board[i]!=0:
                count += abs((length-board[i])-i)
        return count

def create_dominoes_game(rows, cols):
    board = []
    for i in range(rows):
        line=[]
        for j in range(cols):
            line.append(False)
        board.append(line)
    return DominoesGame(board)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if row>=self.rows or col>=self.cols or self.board[row][col]:
            return False
        if vertical:
            if row+1>=self.rows or self.board[row+1][col]:
                return False
        else:
            if col+1>=self.cols or self.board[row][col+1]:
                return False
        return True

    def legal_moves(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i,j,vertical):
                    yield i,j

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row,col,vertical):
            self.board[row][col]=True
            if vertical:
                self.board[row+1][col] = True
            else:
                self.board[row][col+1] = True

    def game_over(self, vertical):
        if list(self.legal_moves(vertical)) != []:
            return False
        return True

    def copy(self):
        result = []
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                line.append(self.board[i][j])
            result.append(line)
        return DominoesGame(result)

    def successors(self, vertical):
        for x,y in self.legal_moves(vertical):
            newboard = self.copy()
            newboard.perform_move(x,y,vertical)
            yield (x,y),newboard

    def get_random_move(self, vertical):
        return random.choice(list(self.legal_moves(vertical)))


    def value(self,vertical):
        mymoves= len(list(self.legal_moves(not vertical)))
        vsmoves= len(list(self.legal_moves(vertical)))
        return mymoves-vsmoves

    def max_ab(self,move,limit,vertical,num,alpha,beta):
        if self.game_over(vertical) or limit==0:
            return move,self.value(vertical),num+1
        result = [None,float("-inf"),None]
        for new_move,newboard in self.successors(vertical):
            newresult = newboard.min_ab(new_move,limit-1,not vertical,num,alpha,beta)
            newvalue = newresult[1]
            num = newresult[2]
            if newvalue > result[1]:
                result = [new_move,newvalue,num]
            else:
                result[2] = num
            if result[1] >= beta:
                return result
            alpha = max([alpha,result[1]])
        return result

    def min_ab(self,move,limit,vertical,num,alpha,beta):
        if self.game_over(vertical) or limit==0:
            return move,self.value(vertical),num+1
        result = [None,float("inf"),None]
        for new_move,newboard in self.successors(vertical):
            newresult = newboard.max_ab(new_move,limit-1,vertical,num,alpha,beta)
            newvalue = newresult[1]
            num = newresult[2]
            if newvalue < result[1]:
                result = [new_move,newvalue,num]
            else:
                result[2] = num
            if result[1] <= alpha:
                return result
            beta = min([beta,result[1]])
        return result

    # Required
    def get_best_move(self, vertical, limit):
        return tuple(self.max_ab(None,limit,vertical,0,float("-inf"),float("inf")))     
    
