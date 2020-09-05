from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from solver.logic.ai import generateBoard, generateMoves
import numpy as np

def generateBoardAndSolve(request):
  num_rows = int(request.GET.get("num_rows"))
  num_cols = int(request.GET.get("num_cols"))
  num_mines = int(request.GET.get("num_mines"))
  board, hidden = generateBoard(num_rows, num_cols, num_mines)
  moves = generateMoves(board, hidden, num_rows, num_cols, num_mines)
  return JsonResponse({'moves': moves, 'board': board.tolist()})