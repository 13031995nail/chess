from django.shortcuts import render
from django.http import HttpResponse
import chess
from .models import Greeting
import re

board = chess.Board()
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'board': 'rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR'})
def index1(request, move):
    board.push_san(move)
    mystr=board.fen()
    mystr=mystr[:mystr.find(" ")]
    mystr = re.sub(r"[/]", "", mystr)
    for i in range(2,9,1):
        stroke = ""
        for j in range(i):
            stroke += str(1)
        mystr = re.sub(str(i), stroke, mystr)
    return render(request, "index.html", {'board': mystr})
