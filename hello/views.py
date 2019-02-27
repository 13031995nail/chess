from django.shortcuts import render
from django.http import HttpResponse
import chess
from .models import Greeting

board = chess.Board()
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")
def index1(request, move):
    board.push_san(move)
    return HttpResponse(board.fen())
