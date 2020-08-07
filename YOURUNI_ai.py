#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Justin Morril (jm5211), Max Wiesenfeld (maw2281), Sahil Shah (ss5848), Kyle Chang ()
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move


############ MINIMAX ###############################

def minimax_min_node(board, color):
  """
  Evaluates min node and returns a utility.
  """
  opp_color = 1 if color == 2 else 2

  min_utility = float("inf")

  moves = get_possible_moves(board, opp_color)
  if not moves: 
    utility = compute_utility(board, color)

  for move in moves:

    #if get_possible_moves(play_move(board, opp_color, move[0], move[1]), color):
    utility = minimax_max_node(play_move(board, opp_color, move[0], move[1]), color)
    #else:
    #  utility = compute_utility(board, opp_color)

    if utility < min_utility:
      min_utility = utility

  return min_utility


def minimax_max_node(board, color):
  """
  Evaluate max node and return utility. 
  """
  max_utility = float("-inf")

  moves = get_possible_moves(board, color)
  if not moves: 
    return compute_utility(board, color)

  for move in moves:

    #if get_possible_moves(play_move(board, color, move[0], move[1]), 3 - color):
    utility = minimax_min_node(play_move(board, color, move[0], move[1]), color)
    #else:
    #  utility = compute_utility(board, color)

    if utility > max_utility:
      max_utility = utility
  
  return max_utility
    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    max_utility = float("-inf")
    best_move = None

    for move in get_possible_moves(board, color):
      i,j = move
      new_board = play_move(board, color, i,j)
      utility = minimax_min_node(new_board, color)
      # select the move that gives the highest utility
      
      if utility > max_utility:
        max_utility = utility
        best_move = (i, j)

    return best_move # returns a move, NOT the best utility. 
    
############ ALPHA-BETA PRUNING #####################

def heuristic_evaluation(board):
  p1_count = 0
  p2_count = 0
  for i in range(len(board)):
    for j in range(len(board)):
      if board[0][0]==1 or board[0][7]==1 or board[7][0]==1 or board[7][7]==1:
        p1_count += 5
      elif board[i][j] == 1 and (j==0 or j==7 or i==0 or i==7):
        p1_count += 2
      else:
        p1_count +=1

      if board[0][0]==2 or board[0][7]==2 or board[7][0]==2 or board[7][7]==2:
        p1_count += 5
      elif board[i][j] == 2 and (j==0 or j==7 or i==0 or i==7):
        p1_count += 2
      else:
        p1_count +=1

    return p1_count-p2_count

  '''
  total = 0
  for row in range(8):
    for tile in range(8):
      points = 1
      if row == 0 or row == 7:
        points += 1
      if tile == 0 or tile == 7:
        points += 2 * points - 1
      
      if tile == color:
        total += points
      elif tile == 3 - color:
        total -= points
  '''

def compute_utility(board):
  return get_score(board)[0] - get_score(board)[1]

def alphabeta_min_node(board, color, alpha, beta, level, limit):
#def alphabeta_min_node(board, color, alpha): 
  
  opp_color = 1 if color == 2 else 2

  min_utility = float("inf")
  
  moves = get_possible_moves(board, opp_color)
  if not moves: 
    return 100 * compute_utility(board, color)

  if level >= limit: 
    #return compute_utility(board, color)
    return heuristic_evaluation(board)

  for move in moves: 
    
    utility = alphabeta_max_node(board, color, alpha, beta, level+1, limit)
  
    if utility < min_utility:
      min_utility = utility
    
    if min_utility<=alpha:
      return min_utility

    beta = min_utility
  return utility

def alphabeta_max_node(board, color, alpha, beta, level, limit):
  
  opp_color = 1 if color == 2 else 2

  max_utility = float("-inf")
  
  moves = get_possible_moves(board, color)
  if not moves:
    return 100 * compute_utility(board, color)
    #return compute_utility(board, color)

  if level >= limit: 
    #return compute_utility(board, color)
    return heuristic_evaluation(board)

  for move in moves: 
    
    utility = alphabeta_min_node(board, color, alpha, beta, level+1, limit)
  
    if utility > max_utility:
      max_utility = utility

    if max_utility>=beta:
      return max_utility
    alpha = max_utility

  return utility

def select_move_alphabeta(board, color): 
  
  max_utility = float("-inf")
  best_move = None

  for move in get_possible_moves(board, color):
    i,j = move
    new_board = play_move(board, color, i,j)
    utility = alphabeta_min_node(new_board, color, 0, float("-inf"), float("inf"), 24)
    # select the move that gives the highest utility
      
    if utility > max_utility:
      max_utility = utility
      best_move = (i, j)

  return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
