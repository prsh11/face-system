import numpy as np
import math
import face_recognition
import json
import cv2
import os


def create_directory(directory: str) -> None:
    """
    Create a directory if it doesn't exist.

    Parameters:
        directory (str): The path of the directory to be created.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    directory = "images"
    # Create 'images' directory if it doesn't exist
    create_directory(directory)

    # Load the pre-trained face cascade classifier

    # Open a connection to the default camera (camera index 0)
    cam = cv2.VideoCapture(0)

    # Set camera dimensions
    cam.set(3, 640)
    cam.set(4, 480)

    # Initialize face capture variables
    count = 0
    face_id = int(input("Enter Face id: "))
    print("\n[INFO] Initializing face capture. Look at the camera and wait...")

    while True:
        # Read a frame from the camera
        ret, img = cam.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        img_copy = np.copy(img)

        faces = face_recognition.face_locations(rgb_small_frame)
        # Process each detected face
        for top, right, bottom, left in faces:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the detected face
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            # Increment the count for naming the saved images
            count += 1

            # Save the captured image into the 'images' directory
            create_directory(f"./images/{face_id}")
            w = abs(left - right)
            h = abs(top - bottom)
            cv2.imwrite(
                f"./images/{face_id}/{count}.jpg",
                img_copy[(top - 50) : (top + h + 50), (left - 50) : (left + w + 50)],
            )

            # Display the image with rectangles around faces
            cv2.imshow("image", img)

        # Press Escape to end the program
        k = cv2.waitKey(100) & 0xFF
        if k < 30:
            break

        # Take 30 face samples and stop video. You may increase or decrease the number of
        # images. The more, the better while training the model.
        elif count >= 30:
            break

    print("\n[INFO] Success! Exiting Program.")

    # Release the camera
    cam.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()
