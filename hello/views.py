from django.shortcuts import render
import chess
import re
import copy
import tensorflow as tf
import numpy as np
import chess.pgn
import random
import itertools
import pickle

board = chess.Board()
moveTotal = 0

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'board': 'rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR'})
def index1(request, move):
    global moveTotal
    if moveTotal % 2 == 1:
        board.push_san(move)
        mystr=board.fen()
        mystr=mystr[:mystr.find(" ")]
        mystr = re.sub(r"[/]", "", mystr)
        for i in range(2,9,1):
            stroke = ""
            for j in range(i):
                stroke += str(1)
            mystr = re.sub(str(i), stroke, mystr)
    else:
        board.push_san(move)
        mystr=board.fen()
        mystr=mystr[:mystr.find(" ")]
        mystr = re.sub(r"[/]", "", mystr)
        for i in range(2, 9, 1):
            stroke = ""
            for j in range(i):
                stroke += str(1)
            mystr = re.sub(str(i), stroke, mystr)
    moveTotal = moveTotal + 1
    return render(request, "index.html", {'board': mystr})