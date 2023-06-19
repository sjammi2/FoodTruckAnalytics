import cv2
import mediapipe as mp
import time

class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)
    
    def findFaces(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(self.imgRGB)

        boundingBoxes = []
        
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                boundingBoxFromClass = detection.location_data.relative_bounding_box

                height, width, channels = img.shape

                # Get location of bounding box
                boundingBox = int(boundingBoxFromClass.xmin * width),  \
                    int(boundingBoxFromClass.ymin * height), int(boundingBoxFromClass.width * width),  \
                    int(boundingBoxFromClass.height * height)
                
                boundingBoxes.append([boundingBox, detection.score])
                
                if draw:
                    img = self.fancyDraw(img, boundingBox)
                
                    cv2.putText(img, f'Score: {int(detection.score[0] * 100)}%', (boundingBox[0] - 20, boundingBox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return img, boundingBoxes
    
    def fancyDraw(self, img, boundingBox, length=30, thickness=5, rectangleThickness=1):
        x, y, width, height = boundingBox
        x1, y1 = x+width, y+height

        cv2.rectangle(img, boundingBox, (0,0,255), rectangleThickness)

        # Top Left of Screen, x,y
        cv2.line(img, (x,y), (x+length, y), (0, 0, 255), thickness)
        cv2.line(img, (x,y), (x, y+length), (0, 0, 255), thickness)

        # Top Right of Screen, x1,y
        cv2.line(img, (x1,y), (x1-length, y), (0, 0, 255), thickness)
        cv2.line(img, (x1,y), (x1, y+length), (0, 0, 255), thickness)

        # Bottom Left of Screen, x,y1
        cv2.line(img, (x,y1), (x+length, y1), (0, 0, 255), thickness)
        cv2.line(img, (x,y1), (x, y1-length), (0, 0, 255), thickness)

        # Top Right of Screen, x1,y1
        cv2.line(img, (x1,y1), (x1-length, y1), (0, 0, 255), thickness)
        cv2.line(img, (x1,y1), (x1, y1-length), (0, 0, 255), thickness)

        return img
    

def main():
    currTime = 0
    prevTime = 0

    detector = FaceDetector()
    cap = cv2.VideoCapture("../Videos/6.mp4")

    while True:
        success, img = cap.read()

        img, boundingBoxes = detector.findFaces(img)

        print(boundingBoxes)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
