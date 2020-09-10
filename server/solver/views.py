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
  moves, segments = generateMoves(board, hidden, num_rows, num_cols, num_mines)
  segments = [[list(tup) for tup in segment] for segment in segments]
  print(segments)

  return JsonResponse({'moves': moves, 'board': board.tolist(), 'segments': segments})