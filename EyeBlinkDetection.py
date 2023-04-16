# Import openCV library
import cv2

# Continously take input from user until he/she chooses to exit
while True:
    
    # Display the available options for the user to choose from
    print("Options:")
    print("1. Live video\n2. Video file\n3. Exit\n")
    option = input("Your option: ")
    
    # option 1: When user wants to count the eye blinks in a live video
    # The live video will be captured at real-time using the webcam of the system
    if option == '1': 
        print("You have choosen live video option ...")
        
        # Create VideoCapture object from OpenCV library to capture video
        # Parameter 0 is used for live video
        video = cv2.VideoCapture(0)
    
    # option 2: When user wants to count the eye blinks in a video that was recorded before and is stored in machine's file system
    elif option == '2':
        print("You have choosen video file option !!. Please type out the video file's path")
        
        # Prompt user to input the file path of the existing video file from webcam
        videoFilePath = input("File Path: ")
        
        print("Reading file at path: ", videoFilePath, " .....")
        
        # Create VideoCapture object from OpenCV library to capture video from existing video file
        # Video file's path must be passed as parameter
        video = cv2.VideoCapture(videoFilePath)
    
    # option 3: To exit
    elif option == '3':
        print("Thank you for using Eye Blink Detection counting. Bye!!")
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
        # capturedFrame: The frame that is captured
        isFrameCaptured, capturedFrame = video.read()
        
        if not isFrameCaptured:
            print("Reached end of the video. Hence exiting ...")
            break 

        # Convert the captured frame(image) to grayscale
        capturedFrame = cv2.cvtColor(capturedFrame, cv2.COLOR_BGR2GRAY)
        
        
        cv2.imshow('EyeBlinkDetector', capturedFrame)
        
        # Check if user has pressed 'q' key. If yes then exit from while loop
        pressedkey = cv2.waitKey(1)
        
        # 113 is the ascii value of 'q'
        if pressedkey == 113:
            break
    
    print("\n ====== Exited from the window. Frame capturing stopped ====== \n")
    # Release the video object(cv2.VideoCapture object)
    video.release()
    cv2.destroyAllWindows()