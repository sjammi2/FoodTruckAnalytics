# Will eventually be the main file for our app

import sqlite3
import cv2
import time
import FaceDetectionModule as fd

con = sqlite3.connect("faces.db") 
cur = con.cursor()

try:
    cur.execute("CREATE TABLE faces(id, timesSeen)")
except sqlite3.OperationalError:
    print('DB already exists.')

currTime = 0
prevTime = 0

detector = fd.FaceDetector()
cap = cv2.VideoCapture(1)

try:
    while True:
        success, img = cap.read()

        img, boundingBoxes = detector.findFaces(img)

        # need to look into facial recognition to recognize how many times a face has been seen

        try:
            if boundingBoxes != []:
                for index, val in enumerate(boundingBoxes):
                    query = "SELECT * FROM faces WHERE id = " + str(index)
                    result = cur.execute(query)
                    t = result.fetchone()

                    i, v = t

                    if v:
                        cur.execute("UPDATE faces SET timesSeen = " + str(v + 1))
                    else:
                        cur.execute(f"INSERT INTO faces VALUES({index}, 1)")

                    con.commit()
        except Exception as e:
            print("Error when inserting into faces")


        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
except KeyboardInterrupt:
    print('Video stream interrupted by keyboard.')
except cv2.error as e:
    print('Video stream interruped, video likely ended. Exception: ' + e)
