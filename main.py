from random import random
from sre_constants import SUCCESS
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
from network import Network
from game import Game
import sys
import numpy as np

def other_id(id):
    if id == 0:
        return 1
    else:
        return 0

useCam = not ('nocam' in sys.argv)

cap = None
detector = None
if useCam:
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    detector = HandDetector(maxHands=1)

initialTime = None
displayedScores = [0,0]
lastWin = None
gameType = int(input("Select game type (AI 1, CONNECT 2): "))
offlineGame = Game
n = None
imgAI = []
id = 1
if gameType == 1:
    offlineGame = Game(0)
elif gameType == 2:
    n = Network(input("Specify server ip address: "))
    id = int(n.getP())

while True:
    if n == None:
        game = offlineGame
    else:
        game = n.send("get")

    imgBG = cv2.imread('Resources/BG.png')
    imgScaled = np.zeros((420,400,4), np.uint8)
    camImg = None
    if useCam:
        SUCCESS, img = cap.read()  
        camImg = cv2.resize(img, (420, 400))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA) 
        imgScaled = cv2.resize(img, (276, 276))
    elif (id == 0 and game.p1Went) or (id == 1 and game.p2Went):
        imgMap = {'R': 1, 'P':2, 'S': 3}
        img = cv2.imread(f'Resources/{imgMap[game.moves[id]]}.png', cv2.IMREAD_UNCHANGED)
        imgScaled = cv2.resize(img, (276, 276))


    # find hands
    hands = None
    playerMove = None
    if useCam:
        hands, img = detector.findHands(camImg)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            if fingers == [0, 0, 0, 0, 0]: # rock
                playerMove = 'R'
                cv2.putText(imgBG, "ROCK", (955,700),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
            if fingers == [1, 1, 1, 1, 1]: # paper
                playerMove = 'P'
                cv2.putText(imgBG, "PAPER", (955,700),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
            if fingers == [0, 1, 1, 0, 0]: # scissors
                playerMove = 'S'
                cv2.putText(imgBG, "SCISSORS", (955,700),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
    else:
        playerMove = cv2.waitKey(1)
        if (playerMove) == ord('r'):
            playerMove = 'R'
        elif (playerMove) == ord('p'):
            playerMove = 'P'
        elif (playerMove) == ord('s'):
            playerMove = 'S'
        else:
            playerMove = None

    if game.canStart() and initialTime == None:
        initialTime = time.time()

    if initialTime != None:
        timer = initialTime + 5 - time.time()
        if timer >= 0:
            cv2.putText(imgBG, str(round(timer, 1)), (570,435),cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

        if timer < 0:
            initialTime = None

            if n == None:
                game.play(other_id(id), 'RPS'[random.randint(0, 2)])

            if game.bothWent():
                displayedScores[0] = game.scores[0]
                displayedScores[1] = game.scores[1]
                lastWin = game.winner()

            if n == None:
                game.reset()
            else:
                game = n.send("reset")

            moveNum = 1
            if game.moves[other_id(id)] == 'P':
                moveNum = 2
            elif game.moves[other_id(id)] == 'S':
                moveNum = 3

            imgAI = cv2.imread(f'Resources/{moveNum}.png', cv2.IMREAD_UNCHANGED)            

    if game.canStart() and (playerMove != None) and (initialTime != None):
        if n == None:
            if not game.p1Went:
                game.play(id, playerMove)
        elif (n != None) and (id == 0 and not game.p1Went) or (id == 1 and not game.p2Went):
            n.send(playerMove)

    imgBG = cvzone.overlayPNG(imgBG, imgScaled, (860, 310))

    if len(imgAI) > 0:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(displayedScores[other_id(id)]), (410,215),cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)
    cv2.putText(imgBG, str(displayedScores[id]), (1112,215),cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)

    if not game.canStart():
        if game.ready[other_id(id)]:
            cv2.putText(imgBG, f'Ready', (200,150),cv2.FONT_HERSHEY_PLAIN, 2, (28, 28, 255), 2)
        if game.ready[id]:
            cv2.putText(imgBG, f'Ready', (900,150),cv2.FONT_HERSHEY_PLAIN, 2, (28, 28, 255), 2)
    
    if lastWin == -1: 
        cv2.putText(imgBG, 'Its a tie!', (505,100),cv2.FONT_HERSHEY_PLAIN, 4, (219, 110, 46), 3)
    elif lastWin == other_id(id):
        cv2.putText(imgBG, 'Opponent wins!', (420,100),cv2.FONT_HERSHEY_PLAIN, 4, (66, 117, 245), 3)
    elif lastWin == id:
        cv2.putText(imgBG, 'You win!', (505,100),cv2.FONT_HERSHEY_PLAIN, 4, (75, 194, 56), 3)

    cv2.imshow('BG', imgBG)
    key = cv2.waitKey(1)
    if key == ord('b'):
        imgAI = []
        initialTime = None
        lastWin = None
        if n == None:
            offlineGame.reset()
            offlineGame.playerReady(0)
            offlineGame.playerReady(1)
        else:
            game = n.send("ready")