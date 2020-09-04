from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from solver.logic import generateBoard, generateMoves

def index(request):
    return HttpResponse("Hello, world.")

def hello(request):
  text = "Hello world"
  num_rows = int(request.GET.get("num_rows"))
  num_cols = int(request.GET.get("num_cols"))
  num_mines = int(request.GET.get("num_mines"))
  board, hidden = generateBoard(num_rows, num_cols, num_mines)
  moves = generateMoves(board, hidden)
  return JsonResponse({'response_text':board.tolist()})
