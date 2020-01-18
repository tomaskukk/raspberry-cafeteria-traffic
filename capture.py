import dropbox
from dropbox.exceptions import ApiError, AuthError
import time
import datetime
import picamera
import sys, os
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)


PHOTOFORMAT = "jpeg"

def camCapture(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        print ("Photo: %s"%filename + "." + PHOTOFORMAT)
        time.sleep(2)
        camera.capture(filename + "." + PHOTOFORMAT, format=PHOTOFORMAT)
        print ("Photo captured and saved")
        return filename + "." + PHOTOFORMAT

def timestamp():
    tstring = datetime.datetime.now()
    print ("Filename generated")
    return tstring.strftime("%Y%m%d_%H%M%S")

def uploadFile(localfile):
#    if (len(TOKEN) == 0):
#        sys.exit("Error: Missing access token")
#
#    print ("creating db object")
#    dbx = dropbox.Dropbox(TOKEN)
#
#    try:
#        dbx.users_get_current_account()
#    except AuthError as err:
#        sys.exit("Error invalid access token")
#
#    uploadPath = "/" + localfile
#
#    with open(localfile, 'rb') as f:
#        print("Uploading " + localfile + " to Dropbox as " + uploadPath + "...")
#
#        try:
#            dbx.files_upload(f.read(), uploadPath)
#        except ApiError as err:
            # Check user has enough Dropbox space quota
#            if (err.error.is_path() and
#                   err.error.get_path().error.is_insufficient_space()):
#                sys.exit("ERROR: Cannot upload; insufficient space.")
#            elif err.user_message_text:
#                print(err.user_message_text)
#                sys.exit()
#            else:
#                print(err)
#                sys.exit()
    # Send the image to remote backend
    url = "http://192.168.1.233:3001/api/traffic/picture"
    files = {'image': open(localfile, 'rb')}
    response = requests.request("POST", url, files=files)
    if (response.status_code == 200):
        print("Picture send succesfully")
    else:
        print("Something went wrong")
#    print(response)

def deleteLocal(file):
    os.system("rm " + file)
    print("File: " + file + " deleted ...")

def doAll():

    # Generate name for file based on current time
    filename = timestamp()

    # Capture photo
    file = camCapture(filename)

    # Upload file
    uploadFile(file)

    # Delete local file
    deleteLocal(file)

    print("Done")
    
def main():
    while 1:
#        if GPIO.input(23) == True:
#            print ("Motion detected")
            doAll()
            time.sleep(60)
#
#       elif GPIO.input(23) == False:
#            print ("No motion detected")
#            time.sleep(1)

if __name__ == "__main__":
    main()
