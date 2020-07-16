# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:38:42 2020

@author: ezhu2
Eli Zhu

"""
import heapq
import copy 

def manhattan(r1,c1,r2,c2): #Used to calculate manhattan distance
    return abs(r1 - r2) + abs((c1-c2))

class Puzzle:
    def __init__(self,board,parent_state = None,previous_move = None):  #Keep track of parents if there are any
        self.board = board # Storing start 
        self.board_string ="" #String representation of board. This is used as a key to keep track of whether a board state was visited
        self.col = 0# Store index of empty node
        self.row = 0
        self.manhattan = 0 # Use compare manhattan distance method to calculate based on goal board
        for i in range(4): #Find the empty spot in the board
            for j in range(4):
                self.board_string += self.board[i][j]
                if(self.board[i][j] == "0"):
                    self.row = i
                    self.col = j
                    
        #Only needed if the current state is  a successor from another puzzle object
        self.parent = parent_state 
        self.previous_move = previous_move

            
    def print_board(self):
        print_val = ""
        for i in self.board:
            line = ""
            for j in i:
                line += (j + " ")
            print(line)
            line += ("\n")
            print_val += line
        print("")
        return print_val
    

    def calc_man_distance(self, goal): # Use this to calculate manhattan distance, relative to the goal
        #This should only be run once, when creating a new board, to compare it to the goal board
        #Manhattan distane should be updated per move, but with different method.
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                for k in range(len(goal.board)):
                    for l in range(len(goal.board)):
                        if(self.board[i][j] == goal.board[k][l]):
                            distance = manhattan(i,j,k,l)
                            self.manhattan += distance

    
    def __lt__(self,other): # Overload comparators based off of manhattan distance for heapq
        return self.manhattan < other.manhattan
    
    def __gt__(self,other):
        return self.manhattan > other.manhattan
    
    def get_prev_move(self): #  Return revious movement, aka how the current state was obtained
        return self.previous_move 
    
def Astar(board,goal):
    frontier = []
    heapq.heappush(frontier,board) #Use heap to keep track of nodes with minimum cost
    visited = {} # Dict to keep track of visited nodes
    generated_count = 0
    while len(frontier) > 0:
        
        current_state = (heapq.heappop(frontier))
        
        if(current_state.manhattan == 0):
            return (current_state,generated_count)
        
        up_board = move_up(current_state,current_state.row,current_state.col)
        if up_board != 0: # If board exists
            if up_board.board_string not in visited:
                generated_count += 1 # Increment count of nodes generated
                up_board.calc_man_distance(goal)#Calculated the manhattan distance
                heapq.heappush(frontier,up_board)
                visited[up_board.board_string] = True #Set node to visited
            
        down_board = move_down(current_state,current_state.row,current_state.col)
        if down_board != 0:  
            if down_board.board_string not in visited:
                generated_count += 1
                down_board.calc_man_distance(goal)
                heapq.heappush(frontier,down_board)
                visited[down_board.board_string] = True

        left_board = move_left(current_state,current_state.row,current_state.col)
        if left_board != 0:
            if left_board.board_string not in visited:
                generated_count += 1
                left_board.calc_man_distance(goal)
                heapq.heappush(frontier,left_board)
                visited[left_board.board_string] = True


            
        right_board = move_right(current_state,current_state.row,current_state.col)
        if right_board != 0:
            if right_board.board_string not in visited:
                generated_count += 1
                right_board.calc_man_distance(goal)
                heapq.heappush(frontier,right_board)
                visited[right_board.board_string] = True

        
    return "Not solvable"

    
# All movement functions return a new puzzle object of the updated board state after the move

def move_up(parent,row,col): #Move empty spot up
    state_copy = copy.deepcopy(parent.board)
    try:
        if (row != 0):
            state_copy[row - 1][col], state_copy[row][col] = state_copy[row][col], state_copy[row - 1][col]
            row -= 1
            return Puzzle(state_copy,parent,"U")
        else:
            raise IndexError
    except IndexError:
        return 0
    
def move_left(parent,row,col): #Move empty spot left
    state_copy = copy.deepcopy(parent.board)
    try:
        if (col != 0):
            state_copy[row][col - 1], state_copy[row][col] = state_copy[row][col], state_copy[row][col - 1]
            col -= 1
            return Puzzle(state_copy,parent,"L")
        else:
            raise IndexError
    except IndexError:
        return 0

def move_down(parent,row,col): #Move empty spot down
    state_copy = copy.deepcopy(parent.board)
    try:
        if (row != 3):
           state_copy[row + 1][col], state_copy[row][col] = state_copy[row][col], state_copy[row + 1][col]
           row += 1
           return Puzzle(state_copy,parent,"D")
        else:
            raise IndexError
    except IndexError:
        return 0

def move_right(parent,row,col): #Move empty spot right
    state_copy = copy.deepcopy(parent.board)
    try:
        if (col != 3):
            state_copy[row][col + 1], state_copy[row][col] = state_copy[row][col], state_copy[row][col + 1]
            col += 1
            return Puzzle(state_copy,parent,"R")
        else:
            raise IndexError
    except IndexError:
        return 0


if __name__ == '__main__':
    read_file = input("Enter name of file to read\n")
    f = open(read_file,'r')
    start_board = []
    line_count = 0 #Iterate through first 4 lines for start, lines 6-9 for goal
    while line_count <= 3:
        curr_line = f.readline()
        tiles = curr_line.split() #Split each line into individual tiles
        start_board.append(tiles)
        line_count += 1
    f.readline()
    line_count = 0
    goal_board = []
    
    while line_count <= 3:
        curr_line = f.readline()
        tiles = curr_line.split() 
        goal_board.append(tiles)
        line_count += 1
        
    start = Puzzle(start_board) #Object for our goal
    goal = Puzzle(goal_board) #Object for our goal
    f.close()
    
    start.calc_man_distance(goal) #Calculate the manhattan distance for the start board
    
    (sol,node_count) =  Astar(start,goal) #Execute our search
    depth = 0
    costs = []
    moves = ""
    #Keeping track of solution 
    while sol.parent:
        moves += sol.get_prev_move() + " " 
        costs.append(sol.manhattan + 1)
        sol = sol.parent
        depth += 1
        
    moves = moves[:-1]
    moves = moves[::-1]
    cost_string = ""
    for cost in costs[::-1]:
        cost_string += str(cost) + " "

    output_file_name = input("Enter output file name\n")
    output_file = open("Output2.txt","w")
    output_file.write(start.print_board())
    output_file.write("\n")
    output_file.write(goal.print_board())
    output_file.write("\n")
    output_file.write(str(depth))
    output_file.write("\n")
    output_file.write(str(node_count))
    output_file.write("\n")
    output_file.write(moves)
    output_file.write("\n")
    output_file.write(cost_string)
    
        