"""

Universal Turing Machine
Rudolf Aelbrecht -- June 2020

A simple universal turing machine implementation.

Example addition machine
(https://www.geeksforgeeks.org/turing-machine-addition/)

input.txt:
00000+000

program.txt:
Q0,0,Q1,X,R
Q0,+,Q5,_,R
Q1,0,Q1,0,R
Q1,+,Q2,+,R
Q2,0,Q2,0,R
Q2,_,Q3,0,L
Q3,0,Q3,0,L
Q3,+,Q4,+,L
Q4,0,Q4,0,L
Q4,X,Q0,X,R

"""

import os
import time

os.system('cls' if os.name == 'nt' else 'clear')

# constants
INPUT = 0
PROGRAM = 1
STATE = 2
NULL = "_"
TAPE_LENGTH = 512
TAPE_START = 64

# tape declaration
tapes = [["_" for _ in range(TAPE_LENGTH)] for _ in range(3)]
heads = [TAPE_START for _ in range(3)]

# statistics variables
head_write_count = 0
head_read_count = 0
tape_write_count = 0
tape_read_count = 0


# retrieve tape symbol at head
def tape_get(tape):
    global tape_read_count
    tape_read_count += 1
    return tapes[tape][heads[tape]]


# set tape symbol at head
def tape_set(tape, v):
    global tape_write_count
    tape_write_count += 1
    tapes[tape][heads[tape]] = v


# get head position
def head_get(tape):
    global head_read_count
    head_read_count += 1
    return heads[tape]


# move head to position
def head_set(tape, i):
    global head_write_count
    head_write_count += 1
    heads[tape] = i


# move head right
def head_right(tape):
    head_set(tape, heads[tape] + 1)


# move head left
def head_left(tape):
    head_set(tape, heads[tape] - 1)


# tape print formatting, show 20 characters of tape around head
def format_tape(tape, head):
    lb = head - 10
    ub = head + 10
    if lb < 0:
        lb = 0
        ub = 20
    if ub > TAPE_LENGTH:
        ub = TAPE_LENGTH
        lb = TAPE_LENGTH - 20
    tape_slice = tape[lb:ub]
    tt = ""
    tt += "   ".join([(" " if (head - lb) != i else "v") for i in range(len(tape_slice))])
    tt += "\n"
    tt += " | ".join([ss for ss in tape_slice])
    return tt


# clear window and print all tapes
def print_tapes():
    os.system('cls' if os.name == 'nt' else 'tput cup 0 0')
    print(format_tape(tapes[0], heads[0]))
    print(format_tape(tapes[1], heads[1]))
    print(format_tape(tapes[2], heads[2]))


# read program
with open("program.txt") as f:
    program = f.read()
    program = program.split("\n")

# read input
with open("input.txt") as f:
    raw_input = f.read()

# store distinct states and symbols in a set
alphabet = set()
states = set()
for t in program:
    if t == "":
        continue
    e = t.split(",")
    states.add(e[0])
    states.add(e[2])
    if e[1] != "_":
        alphabet.add(e[1])
    if e[3] != "_":
        alphabet.add(e[3])
alphabet = sorted(list(alphabet))
states = sorted(list(states))

# create dicts for symbols and states that can be used to encode input
alphabet_d = dict()
for a in alphabet:
    alphabet_d[a] = len(alphabet_d)
states_d = dict()
for s in states:
    states_d[s] = len(states_d)

# write and encode input to tape 1
for t in raw_input:
    if t not in alphabet_d:
        continue
    tapes[0][heads[0]] = t  # str(alphabet_d[t])
    heads[0] += 1
heads[0] = TAPE_START

# write and encode program to tape 2
for t in program:
    if t == "":
        continue
    e = t.split(",")
    h = heads[1]
    tapes[1][h] = str(states_d[e[0]])
    tapes[1][h + 1] = e[1]  # str(alphabet_d[e[1]]) if e[1] != "_" else "_"
    tapes[1][h + 2] = str(states_d[e[2]])
    tapes[1][h + 3] = e[3]  # str(alphabet_d[e[3]]) if e[3] != "_" else "_"
    tapes[1][h + 4] = e[4]
    heads[1] += 5
heads[1] = TAPE_START

# write and encode current state to tape 3
tapes[2][TAPE_START] = str(0)

# run turing machine
while True:

    # halt when no state transition is found
    if tape_get(PROGRAM) == NULL:
        # decode input tape and print
        result = "".join(tapes[0]).replace("_", "")
        output = result  # [alphabet[int(s)] for s in result]
        print("".join(output))

        # stats print
        print("head read/writes: %d/%d" % (head_read_count, head_write_count))
        print("tape read/writes: %d/%d" % (tape_read_count, tape_write_count))

        exit(0)

    # check if state matches
    if tape_get(PROGRAM) != tape_get(STATE):
        for _ in range(5):
            head_right(PROGRAM)
        continue

    head_right(PROGRAM)

    # check if symbol matches
    if tape_get(PROGRAM) != tape_get(INPUT):
        for _ in range(4):
            head_right(PROGRAM)
        continue

    head_right(PROGRAM)

    # update current state
    tape_set(STATE, tape_get(PROGRAM))

    head_right(PROGRAM)

    # update current symbol
    tape_set(INPUT, tape_get(PROGRAM))

    head_right(PROGRAM)

    # move input tape
    if tape_get(PROGRAM) == "R":
        head_right(INPUT)
    elif tape_get(PROGRAM) == "L":
        head_left(INPUT)

    time.sleep(0.1)

    print_tapes()

    # reset program counter
    head_set(PROGRAM, TAPE_START)
