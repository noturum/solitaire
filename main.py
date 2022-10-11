#import pixellib
import os
from ctypes import windll

import pyautogui
import keyboard
from threading import Thread
#from pixellib.torchbackend.instance import instanceSegmentation
import cv2
import numpy as np
'''ins = instanceSegmentation()
ins.load_model("pointrend_resnet50.pkl")
ins.segmentImage("image.jpg", show_bboxes=True, output_image_name="output_image.jpg")'''
complete=0

import win32api,win32con,time
def MouseDownMove(posBegin,posEnd):

    windll.user32.SetCursorPos(int(posBegin[0]), int(posBegin[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE , int(posEnd[0]), int(posEnd[1]))
    time.sleep(0.5)
    windll.user32.SetCursorPos(int(posEnd[0]), int(posEnd[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(posEnd[0]), int(posEnd[1]))
    time.sleep(0.5)
def make_screen():
    return pyautogui.screenshot('screen.jpg')


def loc():
    while True:
        keyboard.wait('shift')
        print(pyautogui.position())

def find_card():
    global complete
    from matplotlib import pyplot as plt
    img_rgb = cv2.imread('screen.jpg')
    field = []
    store = []
    bank = []

    def findCardProc(fl):
        global complete
        for nf in fl:

            template = cv2.imread('card//'+nf, 0)
            w, h = template.shape[::-1]

            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.91
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                print(nf)
                if int(pt[1])>340:

                    field.append({'card':[nf.replace('.png','').split(' ')[0],nf.replace('.png','').split(' ')[1]],'pos':(pt[0]+w/2,pt[1]+h/2)})
                if pt[0]>548 and pt[1]>102 and pt[0]<750 and  pt[1]<291:
                    bank.append({'card':[nf.replace('.png','').split(' ')[0],nf.replace('.png','').split(' ')[1]],'pos':(pt[0]+w/2,pt[1]+h/2)})

                if pt[0]>881 and pt[1]>100 and pt[0]<1546 and pt[1] <284:
                    store.append({'card':[nf.replace('.png','').split(' ')[0],nf.replace('.png','').split(' ')[1]],'pos':(pt[0]+w/2,pt[1]+h/2)})

                break
        #cv2.imwrite('res.png', img_rgb)
        complete+=1
    countOnProc=[12,12,12,12]
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    fileList=os.listdir('card//')
    for i in range(0,51,13):
        if i==51:

            break
        else:
            Thread(target=findCardProc,args=[fileList[i:i+13]]).start()
    import time

    while True:

        if complete==4:
            return field,store,bank
            complete = 0

        time.sleep(0.4)







def drag_drop(posBegin,posEnd):
    pyautogui.moveTo(posBegin[0],posBegin[1])
    pyautogui.dragTo(posEnd[0]+20, posEnd[1],0.2, button='left')

def click():
    pass
def main():
    values=['a','2','3','4','5','6','7','8','9','10','j','q','k']
    black=['p','k']
    red=['c','b']
    stop=False
    keyboard.wait('shift')
    make_screen()
    field=[]

    bank=[]
    store=[]
    field,store,bank=find_card()

    try:
        for firstCard in field:

            for card in field:
                if values.index(card['card'][0])-values.index(firstCard['card'][0])==1:

                    if card['card'][1] in black and firstCard['card'][1] in red:
                        MouseDownMove(firstCard['pos'],card['pos'])
                        raise ValueError
                    if card['card'][1] in red and firstCard['card'][1] in black:
                        MouseDownMove(firstCard['pos'],card['pos'])
                        raise ValueError
    except ValueError:
        print('on')


    pass
if __name__=="__main__":
    main()
