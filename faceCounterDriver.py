# Will count the number faces in a video stream and display them in the image

import cv2
import time
import FaceDetectionModule as fd

def main():
    currTime = 0
    prevTime = 0

    detector = fd.FaceDetector(minDetectionCon=0.3)
    cap = cv2.VideoCapture("./Videos/6.mp4")

    while True:
        success, img = cap.read()

        img, boundingBoxes = detector.findFaces(img)

        numFaces = len(boundingBoxes)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, f'Faces: {int(numFaces)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
