# Import openCV and dlib library
import cv2, dlib

# Import distance from scipy.spatial library for calculating euclidean distance
from scipy.spatial import distance as dist

# Import face_utils from imutils for displaying the border of detected eyes
from imutils import face_utils

# Use get_frontal_face_detector in dlib library to detect faces from a frame
faceDetector = dlib.get_frontal_face_detector()

# Use shape_predictor in dlib library to detect landmarks(eyes, nose e.t.c.) in a provided face
landmarksPredictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# These are the pre-defined landmarks(dlib library) for eyes 
leftEyeLandmarks  = [36, 37, 38, 39, 40, 41]
rightEyeLandmarks = [42, 43, 44, 45, 46, 47]

# areEyesClosed - global variable to detect opening and closing of eyes
areEyesClosed = False

# Method to calculate the midpoint of given two points
def midpoint(p1 ,p2):
    return (p1.x + p2.x)/2,(p1.y + p2.y)/2

# Method to calculate the blink ratio of an eye
def get_blink_ratio_of_eye(points, landmarks):
    rightCornerCoords  = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
    leftCornerCoords   = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    
    bottomCenterCoords = midpoint(landmarks.part(points[5]), landmarks.part(points[4]))
    topCenterCoords    = midpoint(landmarks.part(points[1]), landmarks.part(points[2]))
    
    verticalDistance   = dist.euclidean(bottomCenterCoords, topCenterCoords)
    horizontalDistance = dist.euclidean(rightCornerCoords, leftCornerCoords)

    blinkRatio = horizontalDistance/verticalDistance

    return blinkRatio
    
# Method to calculate the average blink ratio of both the eyes
def find_blink_ratio(left, right, landmarks):
    leftBlinkRatio  = get_blink_ratio_of_eye(left, landmarks)
    rightBlinkRatio = get_blink_ratio_of_eye(right, landmarks)
    
    return (rightBlinkRatio + leftBlinkRatio)/2 

print("Welcome to Eye Blink Detection Counting!! \n")
# Continously take input from user until he/she chooses to exit
while True:
    # eyeBlinkCounter - variable to keep track of the eye blinks count
    eyeBlinkCounter = 0
    
    # Display the available options for the user to choose from
    print("Options:")
    print("1. Live video\n2. Video file\n3. Exit\n")
    print("Please choose your option !!!")
    option = input("Your option: ")
    
    # option 1: When user wants to count the eye blinks in a live video
    # The live video will be captured at real-time using web-cam of the system
    if option == '1': 
        print("You have choose live video option ...")
        
        # Create VideoCapture object from OpenCV library to capture video
        # Parameter 0 is used in the case of live video
        video = cv2.VideoCapture(0)
    
    # option 2: When user wants to count the eye blinks in a video that was recorded before and is stored in machine's file system
    elif option == '2':
        print("You have chosen video file option !!. Please type out the video file's path")
        
        # Prompt user to input the file path of the existing video file from web-cam
        videoFilePath = input("File Path: ")

        print("Reading file at path: ", videoFilePath, " .....")
        
        # Create VideoCapture object from OpenCV library to capture video from existing video file
        # Video file's path must be passed as parameter
        try:
            video = cv2.VideoCapture(videoFilePath)
        except:
            print("No file present at the specified location:", videoFilePath)
    
    # option 3: To exit
    elif option == '3':
        print("\nThank you for using Eye Blink Detection Counting. GoodBye!!")
        break
    
    # If user gives a value which is not there in the provided options, ask again for the valid input
    else:
        print("You have chosen a wrong option value!! Kindly re-enter your choice\n")
        continue
    
    # Create a window with name EyeBlinkDetector
    cv2.namedWindow('EyeBlinkDetector')
    
    # Infinite while loop is used to read the frames from the video continously. 'q' key is to be used to stop frame capture
    while True:
        
        # video.read reads frames and returns the frame and success/failure boolean value
        # isFrameCaptured: Indicates if frame is captured or not
        # capturedFrame: Frame that is captured
        isFrameCaptured, capturedFrame = video.read()
        
        if not isFrameCaptured:
            print("Reached end of the video. Hence exiting ...")
            break 

        # Convert the captured frame(image) to grayscale
        capturedFrame = cv2.cvtColor(capturedFrame, cv2.COLOR_BGR2GRAY)
        
        # Use dlib library to detect and retrieve the faces present in a frame
        detected_faces,_,_ = faceDetector.run(image = capturedFrame, adjust_threshold = 0.0, upsample_num_times = 0)

        #if len(detected_faces) > 1:
          #  print("Only 1 face is supported. More than 1 face detected !!!")
           # cv2.putText(capturedFrame, "{} faces detected !!!".format(len(detected_faces)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #break
        for face in detected_faces:
            landmarks = landmarksPredictor(capturedFrame, face)
            faceBlinkRatio = find_blink_ratio(leftEyeLandmarks, rightEyeLandmarks, landmarks)
            
            # Calculate borders of eyes as Hull
            leftEyeHull = cv2.convexHull(face_utils.shape_to_np(landmarks)[leftEyeLandmarks])
            rightEyeHull = cv2.convexHull(face_utils.shape_to_np(landmarks)[rightEyeLandmarks])
    		
            # Draw the borders of eyes calculated above in the openCV window
            cv2.drawContours(capturedFrame, [leftEyeHull], -1, (255, 0, 0), 1)
            cv2.drawContours(capturedFrame, [rightEyeHull], -1, (255, 0, 0), 1)
            
            # If the calculated blink ratio is more than the specified threshold(5.5), it means eyes are closed
            # value 5.5 is decided after testing with various values
            if faceBlinkRatio > 5.5:
                # make the global variable areEyesClosed value to True once eyes are closed
                areEyesClosed = True
            # When eyes are opened
            elif areEyesClosed:
                cv2.putText(capturedFrame ,"BLINK DETECTED !!!",(20,120), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,0),4,cv2.LINE_AA)
                # increment the eyeblink counter value
                eyeBlinkCounter += 1
                areEyesClosed = False
        
        # Display the total number of eye blinks in the openCV window
        cv2.putText(capturedFrame, "Total blinks: {}".format(eyeBlinkCounter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display the frame in the previously created openCV window
        cv2.imshow('EyeBlinkDetector', capturedFrame)
        
        # Check if user has pressed 'q' key. If yes then exit from while loop
        pressedkey = cv2.waitKey(1)
        
        # 113 is the ascii value of 'q'
        if pressedkey == 113:
            break
    
    print("\n ====== Exited from the window. Frame capturing stopped ====== \n")
    
    print("\n Total number of eye blinks detected: ", eyeBlinkCounter, "\n")
    
    # Release the video object(cv2.VideoCapture object)
    video.release()
    cv2.destroyAllWindows()