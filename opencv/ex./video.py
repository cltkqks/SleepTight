import numpy as np
import cv2
import os



def writeVideo():
    os.system('sudo modprobe bcm2835-v4l2')
    try:
        print('camera on')
        cap=cv2.VideoCapture(0)
    except:
        print('fail')
        return

    fps = 20.0
    width = int(cap.get(3))
    height = int(cap.get(4))
    fcc = cv2.VideoWriter_fourcc('X', '2', '6', '4')

    out = cv2.VideoWriter('mycam.avi', fcc, fps, (width, height))
    print('recording')

    while True:
        if cap.isOpened() == False:
            cap.open()
        ret, frame = cap.read()
        if not ret:
            print('video read error')
            break

        cv2.imshow('video', frame)
        out.write(frame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            print('recording off')
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()




writeVideo()

