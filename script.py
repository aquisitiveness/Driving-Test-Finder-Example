import numpy
import pyautogui
import cv2
import os
import time
import keyboard
import threading
import random


IMAGEFOLDER = "Imgs"

os.chdir(IMAGEFOLDER)

DATE = cv2.cvtColor(cv2.imread("dvsa_target_date.png",cv2.IMREAD_UNCHANGED),cv2.COLOR_RGBA2BGR) # The image of the target date

REFRESH = cv2.cvtColor(cv2.imread("refresh.png",cv2.IMREAD_UNCHANGED),cv2.COLOR_RGBA2BGR) # The image of the button to reload the page

ROBOCHECK = cv2.cvtColor(cv2.imread("stuck.png",cv2.IMREAD_UNCHANGED),cv2.COLOR_RGBA2BGR) # The image of the captcha

def screenshot():
    sc = numpy.array(pyautogui.screenshot("Debug.png",region=(0,0,1920,1080))) # 1920 x 1080 monitor assumed
    return sc
        
def click_when_appears(image, threshold):
    time.sleep(0.3)
    is_present = False

    yOffset = image.shape[0]/2
    xOffset = image.shape[1]/2
    
    while (not is_present):
        sc = screenshot()

        result = cv2.matchTemplate(sc,image,cv2.TM_CCOEFF_NORMED)

        minMax = cv2.minMaxLoc(result)
        if (minMax[1] > threshold):
            pyautogui.click(x= minMax[3][0]+xOffset,y = minMax[3][1]+yOffset)
            time.sleep(0.3)
            print(f"Click successful, Conf: {minMax[1]}")
            return

        
def wait_till_appears(image, threshold, timeout):
    for i in range(timeout):

        sc = screenshot()
        result = cv2.matchTemplate(sc,image,cv2.TM_CCOEFF_NORMED)
        minMax = cv2.minMaxLoc(result)

        if (minMax[1] > threshold):

            print("Waited, Found")
            return True
    print("Waited, Not Found")
    return False

time.sleep(2)

def alter_keys(event):

    if event.event_type == keyboard.KEY_DOWN:
    
        if event.name == "z": # When z is pressed, exit the script
            print("exiting")
            os._exit(1)


def main_loop():

    while True:

        time.sleep(2)

        while (wait_till_appears(ROBOCHECK,0.9,20)):
            os.system("ffplay -nodisp -autoexit -loglevel quiet /usr/share/sounds/freedesktop/stereo/complete.oga") # Alert the user to complete the captcha. Uses a built-in sound from linux


        while (not wait_till_appears(REFRESH,0.9,20)):
            os.system("ffplay -nodisp -autoexit -loglevel quiet /usr/share/sounds/freedesktop/stereo/complete.oga") # Alert the user that the script is stuck. Uses a built-in sound from linux

        time.sleep(2)

        if (wait_till_appears(DATE,0.95,10)):

            time.sleep(4)
            wait_till_appears(DATE,0.95)
            while(True): # Infinite loop
                os.system("ffplay -nodisp -autoexit -loglevel quiet /usr/share/sounds/freedesktop/stereo/complete.oga") # Alert the script has found a date. It will be up to the user to book the date themselves. Uses a built-in sound from linux

        else:
            time.sleep(random.randint(60,120)) # Waits a random amount of time
            pyautogui.click(600,160) # Clicks pre-determined locations, perhaps use click_when_appears?
            time.sleep(3)
            pyautogui.click(400,300) # Clicks pre-determined locations




loop = threading.Thread(target=main_loop)
loop.start()
keyboard.hook(alter_keys)      
    