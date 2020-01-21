import time
import datetime
import picamera
import sys, os
import requests




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
    # Send the image to remote backend
    url = "http://192.168.1.233:3001/api/traffic/picture"
    files = {'image': open(localfile, 'rb')}
    response = requests.request("POST", url, files=files)
    if (response.status_code == 200):
        print("Picture send succesfully")
    else:
        print("Something went wrong")

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
            doAll()
            time.sleep(60)

if __name__ == "__main__":
    main()
