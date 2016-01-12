#!/usr/bin/python3 -u
# http://home.hccnet.nl/h.g.muller/interfacing.txt
import chess
import sys
import logging
import random
import signal

signal.signal(signal.SIGINT, signal.SIG_IGN)

old_print = print
def print(message):
    old_print(message)
    logging.info(message)

def cmd_new(line):
    global board, side, ponder
    board = chess.Board()
    side = chess.BLACK;
    ponder = False

def cmd_go(line):
    global side
    side = board.turn

def cmd_force(line):
    global side
    side = 2

def cmd_quit(line):
    exit()

def cmd_time(line):
    global time
    centiseconds = int(line.split()[1])
    time = centiseconds

def cmd_easy(line):
    global ponder
    ponder = False

def cmd_hard(line):
    global ponder
    ponder = True

def cmd_move(line):
    san_move = line[:5]
    try:
        move = board.parse_san(san_move)
        board.push(move)
    except ValueError:
        print("Illegal move:%s" % line)

def cmd_protover(line):
    for f in [
              'done=0',
              'myname="Randy"',
              'sigint=0',
              'san=1',
              'reuse=1',
              'variants=normal',
              'done=1'
             ]:
        print("feature %s" % f)

supported_commands = [
        #"level",
        "new",
        "force",
        "go",
        "quit",
        "time",
        "hard",
        "easy",
        "protover",
        ]

def make_move():
    move = random.choice(list(board.legal_moves))
    print("move %s" % str(move))
    board.push(move)

logging.basicConfig(filename="transcript.log", level=logging.DEBUG)
cmd_new("")

def main():
    while(True):
        if side == board.turn and not board.is_game_over():
            make_move()
        else:
            line = input()
            logging.info("> %s" % line)
            if line != "":
                if line.split()[0] in supported_commands:
                    eval("cmd_%s(%r)" % (line.split()[0], line))
                elif not board.is_game_over():
                    cmd_move(line)

if __name__ == '__main__':
    main()
