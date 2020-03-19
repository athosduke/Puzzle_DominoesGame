############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Songmeng Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import time
from queue import PriorityQueue
import copy

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    for i in range(rows):
        line =[]
        for j in range(1,cols+1):
            line.append(j+i*cols);
        board.append(line)
    board[rows-1][cols-1] = 0;
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        cols = len(self.board[0])
        self.cols = cols
        self.rows = len(self.board)
        pindex = (sum(board,[])).index(0)
        self.prow = int(pindex/cols)
        self.pcol = pindex%cols
        
    def get_board(self):
        return (self.board)

    def elements(self):
        return sum(self.board,[])

    def h(self):
        elements = sum(self.board,[])
        count = 0
        for i in range(len(elements)-1):
            if elements[i] != i+1:
                irow = self.rows -1;
                icol = self.cols -1;
                if elements[i] != 0:   
                    irow = int((elements[i]-1)/self.cols);
                    icol = (elements[i]-1)%self.cols;
                count += abs(irow-int(i/self.cols)) + abs(icol-i%self.cols);
        last = elements[-1];
        if last != 0:
            count += abs(int(last/self.cols)-(self.cols-1))+abs(last%self.cols-(self.cols-1));
        return count

    def perform_move(self, direction):
        result = False
        prow = self.prow
        pcol = self.pcol
        if (direction == "up"):
            if (self.prow > 0):
                self.prow -= 1
                self.board[prow][pcol] = self.board[prow-1][pcol]
                self.board[prow-1][pcol] = 0 
                result = True
        elif (direction == "down"): 
            if (self.prow < self.rows-1):
                    self.prow += 1
                    self.board[prow][pcol] = self.board[prow+1][pcol]
                    self.board[prow+1][pcol] = 0 
                    result = True
        elif (direction == "left"): 
            if (self.pcol > 0):
                    self.pcol -= 1
                    self.board[prow][pcol] = self.board[prow][pcol-1]
                    self.board[prow][pcol-1] = 0 
                    result = True
        elif (direction == "right"): 
            if (self.pcol < self.cols-1):
                    self.pcol += 1
                    self.board[prow][pcol] = self.board[prow][pcol+1]
                    self.board[prow][pcol+1] = 0 
                    result = True
        return result

    def scramble(self, num_moves):
        directionlist = ["up","down","left","right"]
        i = 1
        while(i < num_move):
            direction = random.choice(directionlist)
            poss = self.perform_move(direction)
            if(poss):
                i+=1


    def is_solved(self):
        if (self.board[self.rows-1][self.cols-1] != 0):
            return False
        elements = sum(self.board,[])
        for i in range(len(elements)-1):
            if (elements[i]!=i+1):
                return False
        return True


    def copy(self):
        copy = []
        for i in self.board:
            line = []
            for j in i:
                line.append(j)
            copy.append(line)
        return TilePuzzle(copy)

    def successors(self):
        for d in ["up","down","left","right"]:
            newboard = self.copy()
            poss = newboard.perform_move(d)
            if(poss):
                yield d, newboard

    def helper_iddfs(self,limit,moves):
        for move,newpuzzle in self.successors():
            moves.append(move)
            if newpuzzle.is_solved():
                yield moves[:]
            if (len(moves)<limit):
                for i in newpuzzle.helper_iddfs(limit,moves):
                    yield i
            moves.pop()

    # Required
    def find_solutions_iddfs(self):
        #start_time = time.time()
        if self.is_solved():
            return []
        fit = False
        for i in range (100):
            for sol in self.helper_iddfs(i,[]):
                if sol is not None:
                    yield sol
                    fit = True
            if fit:
                #print("--- %s seconds ---" % (time.time() - start_time))
                break

    # Required
    def find_solution_a_star(self):
        #start_time = time.time()
        if self.is_solved():
            return []
        depth = 0
        knownboard = []
        knownboard.append(self.board)
        openlist = PriorityQueue()
        f = self.h() + depth
        #        score depth move newboard
        openlist.put((f,(depth,[],self)))
        while not openlist.empty():
            mytuple = openlist.get()
            #f = mytuple[0]
            depth = mytuple[1][0]
            moves = mytuple[1][1]
            newp = mytuple[1][2]
            for move,newpuzzle in newp.successors():
                if(newpuzzle.board) not in knownboard:
                    newmove = copy.copy(moves)
                    newmove.append(move)
                    if newpuzzle.is_solved():
                        #print("--- %s seconds ---" % (time.time() - start_time))
                        return newmove
                    knownboard.append(newpuzzle.board)
                    newdepth = depth+1
                    newf = newpuzzle.h()+ newdepth
                    new_p = newpuzzle.copy()
                    #print(newf,newmove,new_p.get_board(),newdepth)
                    openlist.put((newf,(newdepth,newmove,new_p)))


############################################################
# Section 2: Grid Navigation
############################################################
def find_path(start, goal, scene):
    
    if start==goal or scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None
    
    rows = len(scene)
    cols = len(scene[0])
    
    def grid_successors(pt):
        x = pt[0]
        y = pt[1]
        if x>0 and not scene[x-1][y]:
            yield (x-1,y)
        if x < rows -1 and not scene[x+1][y]:
            yield (x+1,y)
        if y>0 and not scene[x][y-1]:
            yield (x,y-1)
        if y<cols-1 and not scene[x][y+1]:
            yield (x,y+1)
        if x>0 and y>0 and not scene[x-1][y-1]:
            yield (x-1,y-1)
        if x>0 and y<cols-1 and not scene[x-1][y+1]:
            yield (x-1,y+1)
        if x<rows-1 and y>0 and not scene[x+1][y-1]:
            yield (x+1,y-1)
        if x<rows-1 and y<cols-1 and not scene[x+1][y+1]:
            yield (x+1,y+1)

    def euclidean_g(curr, goal):
        return math.sqrt((curr[0]-goal[0])**2 + (curr[1]-goal[1])**2)

    openlist = PriorityQueue()
    path = []
    knownpt = []
    path.append(start)
    knownpt.append(start)
    #                        f            h  path 
    openlist.put((euclidean_g(start,goal),(0,path)))

    while not openlist.empty():
        mytuple = openlist.get()
        depth = mytuple[1][0]
        paths = mytuple[1][1]
        for pt in grid_successors(paths[-1]):
            if pt not in knownpt:
                knownpt.append(pt)
                newpath = copy.copy(paths)
                newpath.append(pt)
                if pt==goal:
                    #print("--- %s seconds ---" % (time.time() - start_time))
                    return newpath
                newh = depth+1
                newf = euclidean_g(pt,goal)+newh
                openlist.put((newf,(newh,newpath)))
    #print("--- %s seconds ---" % (time.time() - start_time))
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

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


############################################################
# Section 4: Dominoes Game
############################################################

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
    
############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
10 hours
"""

feedback_question_2 = """
alpha-beta search is challenging.
last function is the stumbling block
"""

feedback_question_3 = """
getting used to a* search algorithm. like the second one. Would delete either 2 or 3 because it's duplicated
"""
