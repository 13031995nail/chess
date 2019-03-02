from django.shortcuts import render
import chess
from django.views.decorators.csrf import csrf_exempt
import re
import copy
import tensorflow as tf
import numpy as np
import chess.pgn
import random
import itertools
import pickle

board = chess.Board()
depth = 1
moveTotal = 0
tf.reset_default_graph()
imported_meta = tf.train.import_meta_graph("hello/net/model_epoch-0.meta")
# Create your views here.
@csrf_exempt
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'board': 'rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR'})
@csrf_exempt
def index1(request):
    global moveTotal
    if moveTotal % 2 == 1:
        board.push_san(request.POST.values()[0])
        mystr=board.fen()
        mystr=mystr[:mystr.find(" ")]
        mystr = re.sub(r"[/]", "", mystr)
        for i in range(2,9,1):
            stroke = ""
            for j in range(i):
                stroke += str(1)
            mystr = re.sub(str(i), stroke, mystr)
    else:
        mystr = computerMove(board, depth).fen()
        mystr = mystr[:mystr.find(" ")]
        mystr = re.sub(r"[/]", "", mystr)
        for i in range(2, 9, 1):
            stroke = ""
            for j in range(i):
                stroke += str(1)
            mystr = re.sub(str(i), stroke, mystr)
    moveTotal = moveTotal + 1
    return render(request, "index.html", {'board': mystr})

def netPredict(first, second):
    global imported_meta

    x_1 = bitifyFEN(beautifyFEN(first.fen()))
    x_2 = bitifyFEN(beautifyFEN(second.fen()))

    toEval = [[x_1,x_2]]
    with tf.Session() as sess:
        imported_meta.restore(sess, tf.train.latest_checkpoint('hello/net/'))
        result = sess.run("output:0", feed_dict={"input:0": toEval})

    if result[0][0] > result [0][1]:
        return (first, second)
    else:
        return (second, first)

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        return node
    if maximizingPlayer:
        v = -1
        for move in node.legal_moves:
            cur = copy.copy(node)
            cur.push(move)
            if v == -1:
                v = alphabeta(cur, depth-1, alpha, beta, False)
            if alpha == -1:
                alpha = v

            v = netPredict(v, alphabeta(cur, depth-1, alpha, beta, False))[0]
            alpha = netPredict(alpha, v)[0]
            if beta != 1:
                if netPredict(alpha, beta)[0] == alpha:
                    break
        return v
    else:
        # если глубина больше 1
        v = 1
        for move in node.legal_moves:
            cur = copy.copy(node)
            cur.push(move)
            if v == 1:
                v = alphabeta(cur, depth-1, alpha, beta, True)
            if beta == 1:
                beta = v

            v = netPredict(v, alphabeta(cur, depth-1, alpha, beta, True))[1]
            beta = netPredict(beta, v)[1]
            if alpha != -1:
                if netPredict(alpha, beta)[0] == alpha:
                    break
        return v

def computerMove(board, depth):
    alpha = -1
    beta = 1
    v = -1
    # board.legal_moves - все возможные ходы из данного расположения фигур на доске (сеть играет белыми)
    for move in board.legal_moves:
        cur = copy.copy(board)
        cur.push(move)
        if v == -1:
            v = alphabeta(cur, depth-1, alpha, beta, False)
            bestMove = move
            if alpha == -1:
                alpha = v
        else:
            new_v = netPredict(alphabeta(cur, depth-1, alpha, beta, False), v)[0]
            if new_v != v:
                bestMove = move
                v = new_v
            alpha = netPredict(alpha, v)[0]

    board.push(bestMove)
    return board


pieces = {
    'p': 1,
    'P': -1,
    'n': 2,
    'N': -2,
    'b': 3,
    'B': -3,
    'r': 4,
    'R': -4,
    'q': 5,
    'Q': -5,
    'k': 6,
    'K': -6
}


def shortenString(s):
    s = s[:s.rfind(" ")]
    return s;


# Например: f = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
def beautifyFEN(f):
    for i in range(4):
        f = shortenString(f)
    # После цикла: f = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b'
    toMove = f[-1]
    if toMove == 'w':  # если предстоит ход белых
        toMove = 7
    else:
        toMove = -7

    f = shortenString(f)
    # f = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR'
    newf = []

    for char in f:
        if char.isdigit():  # если символ цифра
            for i in range(int(char)):
                newf.append(0)
        elif char != '/':
            newf.append(pieces[char])
    newf.append(toMove)
    return newf


def bitifyFEN(f):  # f - одномерный массив целых чисел от -7 до 7 размера 65
    arrs = []
    result = []
    s = {
        '1': 0,
        '2': 1,
        '3': 2,
        '4': 3,
        '5': 4,
        '6': 5,
        '-1': 6,
        '-2': 7,
        '-3': 8,
        '-4': 9,
        '-5': 10,
        '-6': 11,
    }
    # arrs - массив формы 12x64 (12 определяет количество фигур)
    for i in range(12):
        arrs.append(np.zeros(64))

    for i in range(64):
        c = str(int(f[i]))
        if c != '0':  # если в i-ой позиции доски есть фигура
            c = s[c]
            # c = s[int(round(c))]
            arrs[c][i] = 1

    for i in range(12):
        result.append(arrs[i])

    # возвращает генератор, на каждой итерации возвращает элементы сначала из первого элемента и т. д.
    result = list(itertools.chain.from_iterable(result))

    if f[64] == -7:
        result.append(1)
    else:
        result.append(0)

    return result  # одномерный массив из 0 и 1 размера 769