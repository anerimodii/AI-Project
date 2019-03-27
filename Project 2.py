import numpy as np
import sys
import copy
import time
import math


##################
# SET PARAMETERS #
##################

# Max search time per move in seconds. This is used for iterative deepening
totalSearchTime = 30

###############################################################################

###################
# Get the m value #
###################
# Ask user for the number of elements in a row needed to win (i.e. the m value)
def getMVal(boardSize):
    while True:
          myinput = input("Enter the number in a row you need to win: ")
          
          if (myinput == "x" or myinput == "X"): sys.exit()
          elif myinput.isalpha() == True: 
             print("  --> Enter a number, not a string")
             continue

          kval = int(myinput)
          
          if boardSize < kval or kval<2:
              print("You did not enter a valid integer")
          else: 
              print(" --> You need to get a sequence of " + str(kval) + " to win.")
              return kval;
          

       
##################
# Get board size #
##################
# Ask user for the board size. The board is intially all zeros, and
# a square is equal to 1 if player 1 made an X, and 2 if player 2 made an O.
def getBoardSize():
    while True:
          myinput = input("Enter the board size: ")
          
          if (myinput == "x" or myinput == "X"): sys.exit()
          elif myinput.isalpha() == True: 
             print("  --> Enter a number, not a string")
             continue

          kval = int(myinput)
          if kval>=2:
                print(" --> Board size is " + str(kval) + " by " + str(kval))
                return kval;
          else: print("You did not enter a valid integer")

####################
# Human play moves #
####################
# This prompts the user for the row and column of his/her move.
def humanMoves(inputBoard, playerNumber):
    
    #inputBoard.printBoard()
    
    # User enters the row/column of the move. You can enter x to exit.
    while True:
        
          row = input("Enter the row number of your move (or x to exit): ")
          if row == "x": sys.exit()
          elif row.isalpha() == True: 
             print("  --> Enter a number, not a string")
             continue
         
          col = input("Enter the column number of your move (or x to exit): ")
          if col == "x": sys.exit()         
          elif col.isalpha() == True: 
             print("  --> Enter a number, not a string")
             continue
      
          print("")
          print("You entered row: " + str(row) + " and column: " + str(col))
          answer = input("Is this correct (y/n/x)? ")
          
          if answer == "y" or answer == "Y":
              validMove = inputBoard.validMoveTest(int(row), int(col))
              if validMove == True:
                 inputBoard.makeMove(row, col, playerNumber)
                 inputBoard.printBoard()
                 break
              else: 
                 print("")
                 print("That is not a valid move!!!")
          elif answer == "x" or answer == "X":
              sys.exit()
           
    # If the plyer won, or the board is full, quit. Otherwise, return the 
    # board object
    if inputBoard.goalTest()==True:
  
       playerNum = inputBoard.getBoardValue(int(row), int(col))
       inputBoard.printBoard()
       if playerNum==1: XorO = "X"
       else: XorO = "O"
       
       print("")
       print("")
       print("")
       print("   --> Game Over. Player " + XorO + " wins.")
       print("")
       print("")      
       print("")
       
  
       sys.exit()
       
    # Else if the board is now full, quit.
    elif inputBoard.boardIsFull()==True: 
        inputBoard.printBoard()
        print("The game is Draw")
        sys.exit()
    else: return inputBoard; 
      
############
# AI Moves #
############  
# Arguments: The board object, and the player number (1 or 2)
# Returns: The board object with the AI's move input.
# The loop checks every possible move the AI could make and chooses the move 
# with the highest heuristic value. 
def computerMoves(inputBoard, playerNumber):
        global heuristicVal
        
        # Keep track of the best heuristic score found.
        # We may want to make this negative infinity
        highestScore = float('-inf')
        
        # This flag is set to 1 when a heuristic value is found that is better
        # than the variable's initialized value.
        flag=0
        
        #Initialize these two vars because if no optimal move is found, we will know.
        rowMove = -1 
        colMove = -1
        
        # We want the total search process to take the amount specified in the
        # totalSearchTime variable. Since we loop through each possible move,
        # we need to compute the maximum search time for each move. 
        timeLimitPerSquare = totalSearchTime/inputBoard.freeSquares
        
        ################################
        # Loop for every possible move #
        ################################
        valid = np.argwhere(inputBoard.matrix == 0) 
        
        for row, col in valid:

                   rowMove=row
                   colMove=col
                    
                   # Make a copy of the Board object, and have the AI make
                   # its move in the square we're looping for.
                   newBoard = copy.deepcopy(inputBoard)
                   newBoard.makeMove(row, col, playerNumber)

                   # The information is needed to set a depth limit and do 
                   # iterative deepending search
                   numberFreeSquares = newBoard.freeSquares                                 
                   iterativeDeepeningDepth = 2 # start at 2
                   start = time.time()
                   runTime = 0
                   
                   ##################################
                   ### ITERATIVE DEEPENING SEARCH ###
                   ##################################
                   
                   # The search should have a maximum depth of the number of 
                   # empty squares on the board.
                   while (runTime<timeLimitPerSquare and
                          iterativeDeepeningDepth<=numberFreeSquares):
                       
                         # Increment the depth limit for iterative deepening
                         iterativeDeepeningDepth += 1

                         # Run minimax function
                         heuristicVal = minimax(newBoard, 
                                                depth=0,                                                 
                                                maximize=False, 
                                                maxDepth=iterativeDeepeningDepth, 
                                                playerNumber=2,
                                                alpha=float('-inf'), 
                                                beta=float('inf')) 
                         
                         # Update the run time       
                         end = time.time()
                         runTime = end - start       
                   
                   # Delete the copied board to avoid any problems
                   del newBoard
                   
                   #if heuristic value>highest.score then save move.
                   print(" --> Heuristic value for row ", row, " and col ",
                         col, " is ", str(round(heuristicVal)), 
                         ". Search depth is ", str(iterativeDeepeningDepth))
                   
                   # If the heuristic value is higher than the prior best,
                   # keep track of the move.
                   if heuristicVal>highestScore:
                      highestScore = heuristicVal
                      bestMoveRow = row
                      bestMoveCol = col
                      flag=1

        #################################################
        ### MAKE ANY MOVE IF NO OPTIMAL MOVE IS FOUND ###
        #################################################
        # Sometimes, every move checked has the same heuristic value. In that
        # case, make the first available move.
        if flag==0:
           bestMoveRow = rowMove
           bestMoveCol = colMove

        # Actually make the best move found
        inputBoard.makeMove(bestMoveRow, bestMoveCol, playerNumber)
 
        ###################################################
        ### END GAME IF A PLAYER WINS, OTHERWISE RETURN ###
        ###################################################
        
        inputBoard.printBoard()    
        
        gameOver = inputBoard.goalTest()
         
        if gameOver:

           playerNum = inputBoard.getBoardValue(bestMoveRow, bestMoveCol)
       
           if playerNum==1: XorO = "X"
           else: XorO = "O"
       
           print("")
           print("")
           print("")
           print("   --> Game Over. Player " + XorO + " wins.")
           print("")
           print("")      
           print("")
       
           sys.exit()
       
        #################################
        ### END GAME IF BOARD IS FULL ###
        #################################
        
        elif inputBoard.boardIsFull()==True: sys.exit()
        
        else: return inputBoard;
      

#################
# getStatesList #
#################
# This accepts a board object as an argument, and returns a LIST of all possible
# next moves. The object input knows which player made the last move.
def getStatesList(inputBoard):

    L = []
     
    # Loop for each possible move on the board. Find all legal moves (i.e. matrix
    # elements that equal zero)
    for row in range(0, inputBoard.boardLength):
            
        for col in range(0, inputBoard.boardLength):
                
            # IF NOT A VALID MOVE, GO TO NEXT ITERATION
            if inputBoard.validMoveTest(row, col)==False: 
               continue
            else:
                
               # CREATE COPY OF CURRENT BOARD 
               newBoard = copy.deepcopy(inputBoard)
               
               # MAKE THE NEXT POSSIBLE MOVE ON THE COPIED BOARD
               newBoard.makeMove(row, col, newBoard.getNextPlayerToMove())
               
               # CHECK TO SEE IF COPIED BOARD WITH MOVE IS IN TERMINAL STATE
               # THIS UPATES THE ATTRIBUTES OF THE BOARD
               newBoard.goalTest()
               
               # Add new board to the list if it is a valid move
               L.append(newBoard)

               # Debugging
               if False:
                  print(" There are ", str(len(L)), "items in list:")
                  newBoard.printBoard()
               
               # DELETE THE BOARD- WE NO LONGER NEED IT
               del newBoard
               
    return L   
    
##################
# MINIMAX SEARCH #
##################   
# Inputs are the board, the tree depth, whether a max or min node, and 
# player number. Player #1 is human, player #2 is AI.
# Function returns the best heuristic value
def minimax(inputBoard, depth, maximize, maxDepth, playerNumber, alpha, beta): 
       
       # debugging
       if False:
           print("  --> Running MINIMAX for Depth:", str(depth), 
             "  Max?:", str(maximize), "   Player Number:", playerNumber)
           inputBoard.printBoard()
           print("")
    
       #################
       ### BASE CASE ###
       #################

       if ((depth>=maxDepth) or
           (inputBoard.goalTest() == True) or
           (inputBoard.boardIsFull() == True)): 

             # Return heuristic value of node
             return Evaluate(inputBoard, playerNumber, depth)
           
       #####################
       # MAXIMIZING PLAYER #
       #####################
       if maximize==True:
           
          # debugging
          if False:
             print("  --> Finding Max at Depth:", str(depth))
             inputBoard.printBoard()
           
          maxVal = float('-inf')
          
          # Get all possible states
          states = getStatesList(inputBoard)
          
          # find next valid move for other player
          for child in states:
              
              val = minimax(child, depth+1, False, maxDepth, playerNumber, alpha, beta)
              
              # Alpha-beta pruning
              if val>=beta: return val
              alpha = max(alpha, val)
              
              # update max value
              if val>maxVal: maxVal=val
              
          return maxVal
          
       #####################
       # MINIMIZING PLAYER #
       #####################
       else:
          
          # debugginfg
          if False: 
             print("  --> Finding Min at Depth:", str(depth))
             inputBoard.printBoard()
           
          minVal = float('inf')
          
          # Get all possible states
          states = getStatesList(inputBoard)
          
          # find next valid move for other player
          for child in states:
              
              val = minimax(child, depth+1, True, maxDepth, playerNumber, alpha, beta)
              
              # Alpha-beta pruning
              if val<=alpha: return val
              beta= min(beta, val)
              
              # update max value
              if val<minVal: minVal=val
              
          return minVal
      
    
#######################
# EVALUATION FUNCTION #
#######################
# Evaluation function that takes a board and the player number (player 1=X 
# and player 2 = O), and returns the utility value of the board 
# for the input player. The utility can range from _ to _?
# The function checks for wins vertically, horizontlly, and along both diagonals
def Evaluate(inputBoard, inputPlayerNumber, depth):
    
    ###############################
    ### CASES WHEN GAME IS OVER ###
    ###############################
    
    if inputBoard.gameOver:
        
       ## WIN/LOSSS, which get positive/negative utility. We divide by the depth to give a higher weight to wins/losses higher up in the search tree vs. lower down in the tree.
       if inputBoard.winningPlayerExists == True:
           if inputBoard.winningPlayerNumber == inputPlayerNumber: utility = 1000000/(1+depth)#float('inf')
           else: utility = -1000000/(depth+1) #float('-inf')
       ## DRAW
       elif inputBoard.boardIsFull()==True: utility = 0
      
    ###########################################
    ### GET UTILITY FOR NON-TERMINAL STATES ###
    ###########################################     
       
    else: 
        
       utility = nonTerminalStateUtility(inputBoard, inputPlayerNumber)
       
    ########################
    ### PRINT AND RETURN###
    ########################
    
    # debugging
    if False:
       print(" Running evalution function, with input player:", str(inputPlayerNumber))
       print(" The board below was assigned the following utility:", str(utility))
       inputBoard.printBoard()
    
    return utility

#############################
# ESTIMATE UTILITY FUNCTION #
#############################
# This estimates the utility of non-terminal states, for the input player number.
def nonTerminalStateUtility(inputBoard, inputPlayerNumber):

      count = 0

      next = inputBoard.getNextPlayerToMove()

      for i in range(inputBoard.boardLength):

         if np.all(inputBoard.matrix[:, i] != next):
             count += 1
         if np.any(inputBoard.matrix[:, i] == inputPlayerNumber):
             count += 1  
         if np.any(inputBoard.matrix[:, i] == next):
             count -= 2

         if np.all(inputBoard.matrix[i, :] != next):
             count += 1
         if np.any(inputBoard.matrix[i, :] == inputPlayerNumber):
             count += 1
         if np.any(inputBoard.matrix[i, :] == next):
             count -= 2   


      if np.all(inputBoard.matrix.diagonal()) != next:
         count += 1
      if np.any(inputBoard.matrix.diagonal()) == next:
         count -= 2 
      if np.all(inputBoard.matrix[:, ::-1].diagonal()) != next:
         count += 1
      if np.any(inputBoard.matrix[:, ::-1].diagonal()) == next:      
         count -= 2
    
      count2=0
      
      # Count the number of moves the player has in the middle of the board
      start = math.ceil(inputBoard.boardLength/3)
      end = inputBoard.boardLength-start
      
      for row in range(start, end):
          for col in range(start, end):
              if inputBoard.matrix[row, col] == next: count2 += 1
              #print("    --> Row:", str(row), "Col:", str(col))       
         
      return count + count2
   
######################
# DEFINE BOARD CLASS #
######################
# The class defined for the game board. It stores the game matrix, which is
# initially set to all zeros, and is equal to either 1 (x) or 2 (o) when each player 
# makes a move. It also keeps tracks of the number of moves, the number of free
# squares, where the last move made was and which player made it, and whether
# a player won, and who the winner player was.
class Board:
      def __init__(self, size):
          self.matrix = np.zeros((size, size))
          self.numberOfSquares = size*size
          self.freeSquares = self.numberOfSquares
          self.numMoves=0
          self.boardLength=size
          self.lastColMove=None
          self.lastRowMove=None
          self.lastPlayerToMove = None
          self.winningPlayerNumber=None
          self.winningPlayerExists=False
          self.gameOver=False
       
      # Method for making a move. Update the last move made info.
      def makeMove(self, row, col, playerNumber):
          
          if self.gameOver==False and self.freeSquares>0:
             self.matrix[int(row), int(col)] = int(playerNumber)
             self.lastRowMove = row
             self.lastColMove = col
             self.lastPlayerToMove = playerNumber
             self.numMoves+=1
             self.freeSquares = self.numberOfSquares-self.numMoves
             
             if self.freeSquares==0: self.gameOver=True
             
          else: print("Can't make move! Game is over!")
       
      # Return the row and col of the last move made
      def getLastMove(self):
          return (self.lastRowMove, self.lastColMove)
      
      # Return the number of the player that is next to move
      def getNextPlayerToMove(self):
          if self.lastPlayerToMove==1: return 2
          else: return 1
      
      # Return whether the board is full (has no more available moves) or not
      def boardIsFull(self):
          return np.all(self.matrix != 0)
         
      # For an input row and column, return the number of the player for that
      # square (or zero if no player moved there yet)
      def getBoardValue(self, row, col):
          return self.matrix[row, col]
      
      # Check whether a given square on the board is free
      def validMoveTest(self, row, col):
          if row >= self.boardLength or col >= self.boardLength:
             return False
          return self.matrix[row, col] == 0

      # print the current state of the game board
      def printBoard(self):
    
          print("")
          print("\033[1;32;40m" + "-"*(self.boardLength*6), "   ")
          
          for row in range(0, self.boardLength):
        
              print("-"*(self.boardLength*6), "   ")
        
              for column in range(0, self.boardLength):
                  if column==0: print("||", end="")
                  item = int(self.matrix[row, column])
            
                  if item==1: 
                     toPrint="X"
                  elif item==2: 
                     toPrint="O"
                  else: toPrint=" "
                
                  print(" ", toPrint, "|", end="")
            
                  if column==self.boardLength-1: print("| " + str(row))
        
          print("-"*(self.boardLength*6), "   ")
          print("-"*(self.boardLength*6), "   ")
    
          for column in range(0, self.boardLength):
              if column==0: print("    " + str(column) + " ", end="")
              else: print("   " + str(column) + " ", end="")
        
          print(" ")
          print(" ")  
          
      # Check whether the last player to move won the game
      def goalTest(self):
    
          val = self.lastPlayerToMove
    
          # Count how many in a row we have.
          horizontalScore = 1
          verticalScore = 1
          rightDiagonalScore = 1
          leftDiagonalScore = 1
    
          ##############
          # Move right #
          ##############
    
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)    
    
          while True:
              if tmpCol+1 > self.boardLength-1: break
              else:
                 tmpCol += 1
                 tmpVal = self.matrix[tmpRow, tmpCol]
                 if tmpVal == val: 
                    horizontalScore += 1
                 else: 
                    break
         
          #############
          # Move left #
          #############
    
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)
    
          while True:
             if tmpCol-1<0: break
             else:
                tmpCol -= 1
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   horizontalScore += 1
                else: 
                   break  
    
          ###########
          # Move up #
          ###########
    
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)  
    
          while True:
             if tmpRow+1>self.boardLength-1: break
             else:
                tmpRow += 1
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   verticalScore += 1
                else: 
                   break

          #############
          # Move down #
          #############
          
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)   
    
          while True:
             if tmpRow-1<0: break
             else: 
                tmpRow -= 1
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   verticalScore += 1
                else: 
                   break   
               
          ##########################
          # Move Up Right Diagonal #
          ##########################
          
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)   
    
          while True:
             if (tmpRow+1>self.boardLength-1) or (tmpCol+1>self.boardLength-1): break
             else: 
                tmpRow += 1
                tmpCol += 1               
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   rightDiagonalScore += 1
                else: 
                   break   
               
          ###########################
          # Move Down Left Diagonal #
          ###########################
          
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)   
    
          while True:
             if (tmpRow-1<0) or (tmpCol-1<0): break
             else: 
                tmpRow -= 1
                tmpCol -= 1               
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   rightDiagonalScore += 1
                else: 
                   break      
               
          #########################
          # Move Up Left Diagonal #
          #########################
          
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)   
    
          while True:
             if (tmpRow+1>self.boardLength-1) or (tmpCol-1<0): break
             else: 
                tmpRow += 1
                tmpCol -= 1               
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   leftDiagonalScore += 1
                else: 
                   break   
               
          ############################
          # Move Down Right Diagonal #
          ############################
          
          tmpCol = int(self.lastColMove)
          tmpRow = int(self.lastRowMove)   
    
          while True:
             if (tmpRow-1<0) or (tmpCol+1>self.boardLength-1): break
             else: 
                tmpRow -= 1
                tmpCol += 1               
                tmpVal = self.matrix[tmpRow, tmpCol]
                if tmpVal==val: 
                   leftDiagonalScore += 1
                else: 
                   break              

    
          if ((horizontalScore >= MVal) or 
              (verticalScore >= MVal) or
              (rightDiagonalScore >= MVal) or
              (leftDiagonalScore >= MVal)): 
              
              # debugging
              if False:
                  #print("   --> Your score is " + str(score))
                  print("")
                  print("GOAL!! Player #", self.lastPlayerToMove, " wins")
                  print("")
              
              self.winningPlayerNumber = self.lastPlayerToMove
              self.winningPlayerExists = True
              self.gameOver = True
              
              return True
          
          else: return False

def firstPlayer():

   first = input("Do you play first(y/n/x)?")
   if first == "y":
       return 1
   elif first == "n":
       return 2
   elif first == "x":
       sys.exit()
   else:
       print("Please enter a valid answer")

###############################################################################
###############################################################################
###############################################################################

# User enters the size of the board
boardSize = getBoardSize()

MVal = getMVal(boardSize)

# Create instance of the game board
Board=Board(boardSize)
Board.printBoard()
first = firstPlayer()
if first == 1:
   while True:
       # player #1 (X's) moves - prompt user for x,y coord.
       # update board. goal test
       # if humanPlayer == 1:
       # player #1 (X's) moves - prompt user for x,y coord.
       # update board. goal test

       Board = humanMoves(Board, playerNumber=1)

       # player #1 (O's) moves - prompt user for x,y coord.
       # update board. goal test
       Board = computerMoves(Board, playerNumber=2)
else:
   while True:
       Board = computerMoves(Board, playerNumber = 2)
       Board = humanMoves(Board, playerNumber = 1)

   
