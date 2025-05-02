"""camera_pid controller."""

from controller import Display, Keyboard, Robot, Camera
from vehicle import Car, Driver
import numpy as np
import cv2
from datetime import datetime
import os
import math

#Getting image from camera
def get_image(camera):
    raw_image = camera.getImage()  
    image = np.frombuffer(raw_image, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4)
    )
    return image

#Image processing functions
def greyscale_cv2(image):
    # Convert BGR image to grayscale
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_img

def rgb_cv2(image):
    # Convert BGR image to RGB
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_img

def canny_cv2(grey_image):
    # Apply Canny edge detection
    edges = cv2.Canny(grey_image, 10,120)
    return edges

def gaussian_blur(image):
    # Apply 3x3 Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(image, (3, 3), 0, 0)
    return blur

def show_hough_lines(img):
    """
    Detects and draws lane lines in an image using the Hough transform.
    
    Process:
    1. Converts image to RGB and grayscale
    2. Applies Gaussian blur to reduce noise
    3. Detects edges using Canny algorithm
    4. Creates a trapezoid mask to focus on road region
    5. Uses Hough transform to detect lines in masked image
    6. Draws detected lines in blue
    
    Args:
        img: Input image to process
        
    Returns:
        img_mask: The masked edge detection image
        lines: Detected line segments from Hough transform
    """
    # Convert image to RGB and grayscale for processing
    rgb = rgb_cv2(img)
    gray = greyscale_cv2(img)
    blur = gaussian_blur(gray)
    canny = canny_cv2(blur)
    
    # Create trapezoid mask to isolate road region
    # Points form a trapezoid shape covering the road area
    #vertices = np.array([[50, 128], [85, 80], [171, 80], [206, 128]], np.int32)
    vertices = np.array([[60, 120], [100, 90], [156, 90], [196, 120]], np.int32)
    img_ro1 = np.zeros_like(gray)
    cv2.fillPoly(img_ro1, [vertices], 255)
    img_mask = cv2.bitwise_and(canny, img_ro1)
    
    # Apply probabilistic Hough transform to detect line segments
    # Parameters:
    # - rho=2: Distance resolution in pixels
    # - theta=pi/180: Angle resolution in radians 
    # - threshold=40: Minimum number of intersections to detect a line
    # - minLineLength=50: Minimum length of line
    # - maxLineGap=10: Maximum gap between line segments to connect them
    lines = cv2.HoughLinesP(img_mask, 2, np.pi / 180, 40, minLineLength=50, maxLineGap=10)
    
    # Create empty image to draw detected lines
    img_lines = np.zeros_like((img_mask.shape[0], img_mask.shape[1], 3), dtype=np.uint8)
    
    # Draw each detected line segment in blue color
    if lines is not None:
       for line in lines:
           x1, y1, x2, y2 = line[0]  # Extract line endpoint coordinates
           cv2.line(img_lines, (x1, y1), (x2, y2), (255, 0, 0), 1)

    return img_mask, lines

#Display image 
def display_image(display, image):
    # Image to display
    image_rgb = np.dstack((image, image,image,))
    # Display image
    image_ref = display.imageNew(
        image_rgb.tobytes(),
        Display.RGB,
        width=image_rgb.shape[1],
        height=image_rgb.shape[0],
    )
    display.imagePaste(image_ref, 0, 0, False)

#initial angle and speed 
manual_steering = 0
steering_angle = 0
angle = 0.0
speed = 5

# set target speed
def set_speed(kmh):
    global speed            #robot.step(50)
#update steering angle
def set_steering_angle(wheel_angle):
    global angle, steering_angle
    # Check limits of steering
    if (wheel_angle - steering_angle) > 0.1:
        wheel_angle = steering_angle + 0.1
    if (wheel_angle - steering_angle) < -0.1:
        wheel_angle = steering_angle - 0.1
    steering_angle = wheel_angle
  
    # limit range of the steering angle
    if wheel_angle > 0.5:
        wheel_angle = 0.5
    elif wheel_angle < -0.5:
        wheel_angle = -0.5
    # update steering angle
    angle = wheel_angle

#validate increment of steering angle
def change_steer_angle(inc):
    global manual_steering
    # Apply increment
    new_manual_steering = manual_steering + inc
    # Validate interval 
    if new_manual_steering <= 25.0 and new_manual_steering >= -25.0: 
        manual_steering = new_manual_steering
        set_steering_angle(manual_steering * 0.02)
    # Debugging
    if manual_steering == 0:
        print("going straight")
    else:
        turn = "left" if steering_angle < 0 else "right"
        #print("turning {} rad {}".format(str(steering_angle),turn))

# main
def main():
    # Create the Robot instance.
    robot = Car()
    driver = Driver()

    # Get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    # Create camera instance
    camera = robot.getDevice("camera")
    camera.enable(timestep)  # timestep

    # processing display
    display_img = Display("display_image")

    #create keyboard instance
    keyboard=Keyboard()
    keyboard.enable(timestep)

    while robot.step() != -1:
        # Get image from camera
        image = get_image(camera)

        # Process and display image
        hough_image_lines, lines = show_hough_lines(image)
        if lines is None:
            change_steer_angle(0.0)
            angle = 0.0  # Set default angle when no lines detected
        else:
            print("Lines detected: ", lines)
            weighted_angle_sum = 0
            weight_sum = 0
            image_height = image.shape[0] # Get image height to calculate weight

            for line in lines:
                x1, y1, x2, y2 = line[0]
                line_angle = math.atan2(y2 - y1, x2 - x1)
                angle_deg = math.degrees(line_angle)

                if angle_deg > 90:
                    angle_deg -= 180
                elif angle_deg < -90:
                    angle_deg += 180

                print("Line angle: ", angle_deg)

                # Example: Weight based on the average y-coordinate (closer to bottom = higher weight)
                weight = 1.0 - ( (y1 + y2) / 2.0 ) / image_height
                weighted_angle_sum += angle_deg * weight
                weight_sum += weight

            if weight_sum > 0:
                avg_weighted_angle = weighted_angle_sum / weight_sum
                steering = -avg_weighted_angle / 90
                change_steer_angle(steering)
                angle = steering  # Set angle based on steering calculation
                print(f"Setting steering to {steering} based on weighted average angle")
            else:
                change_steer_angle(0.0)
                angle = 0.0  # Set default angle when weight sum is 0

        display_image(display_img, hough_image_lines)

        # Read keyboard
        key=keyboard.getKey()
        if key == keyboard.UP: #up
            set_speed(speed + 5.0)
            print("up")
        elif key == keyboard.DOWN: #down
            set_speed(speed - 5.0)
            print("down")
        elif key == ord('A'):
            #filename with timestamp and saved in current directory
            current_datetime = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
            file_name = current_datetime + ".png"
            print("Image taken")
            camera.saveImage(os.getcwd() + "/" + file_name, 1)
            
        #update angle and speed
        driver.setSteeringAngle(angle)
        driver.setCruisingSpeed(speed)


if __name__ == "__main__":
    main()