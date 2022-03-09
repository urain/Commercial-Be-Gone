# COMMERCIAL-BE-GONE
#
# DESCRIPTION: While streaming news for example, this program can automatically mute audio when it detects that commercials are playing i.e. While watching CNN, Fox, etc; the news logo is always visible while the program is active. However, when it cuts to commercial the logo disappears.
#
# MACOS:
# Confirmed working for MacOS using Google Chrome
# sudo pip3 install comtypes opencv-python numpy matplotlib Pillow
#
# WINDOWS:
# Confirmed working for Microsoft Windows using Microsoft Edge.
# pip3 install pycaw comtypes opencv-python numpy matplotlib Pillow
#
# LINUX:
# Haven't implemented a solution yet.
#
# NOTE: You need to disable Hardware Acceleration in Google Chrome (MacOS) or Microsoft Edge (Windows) for HDCP copyright protection to allow screenshots to capture a still image of the streaming service, in this case CNN News Stream. Otherwise your secreenshots will be black if your video device and HDMI cable support HDCP and the service you are streaming has HDCP copyright protection enabled.
#
# NOTE: You need to take a cropped snapshot of the logo you want, rename it to logo.png, and place it in the program folder.
#
# NOTE: The logo for the news channel needs to be visible on the screen somewhere i.e. if you were to take a screenshot you would need to be able to find it with your own eyes.

#--------------------------------------------------------------
# Controlling audio
#
import os
from sys import platform
myPlatform = platform.lower()

# Windows specific imports and decodes the Nirsoft tool Nircmd for muting audio per application.
if "win32" in myPlatform:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    # This is a little sketchy, but if I base64 encode the binary, it can't be transported via email because of "virus" scanners etc. If I xor obfuscate the binary, same thing. However, if I add an ascii header to the the b64 or binary data, no issues. mkkkkayyy....
    import base64
    f = open("nircmd","rb")
    nircmd = f.read()
    f.close()
    fakeHeader = b"Good morning and welcome to\n"
    f = open("nircmd.exe","wb")
    f.write(base64.b64decode(nircmd.replace(fakeHeader,b"")))
    f.close()

savedSoundLevel = ""
def controlSound(level):
    global savedSoundLevel
    
    # Microsoft Windows
    if "win32" in myPlatform:

        # SOLUTION 1: Mute all audio. Not a great solution if you're listening to multiple things.
        '''
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Control volume
        if level=="unmute":
            volume.SetMasterVolumeLevel(savedSoundLevel, None) #max
        elif level=="mute":
            savedSoundLevel = volume.GetMasterVolumeLevel()
            volume.SetMasterVolumeLevel(-30, None) # almost zero
        '''
            
        # SOLUTION 2: Powershell command to execute B64 directly to get around quote encoding issues. Often flagged by email scanners for "sketchy" behavior...fair.
        '''
        $base64Cmd = 
          [System.Convert]::ToBase64String(
             [System.Text.Encoding]::Unicode.GetBytes(
               '$wshell=New-Object -ComObject wscript.shell;$wshell.AppActivate("Edge");$wshell.SendKeys("^m");'
             )
          )
        Write-host $base64Cmd
        '''
        # This command will find Microsoft Edge browser and send the key commands CTRL+M which will
        # mute the current tab.
        #os.system("powershell -EncodedCommand JAB3AHMAaABlAGwAbAA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAEMAbwBtAE8AYgBqAGUAYwB0ACAAdwBzAGMAcgBpAHAAdAAuAHMAaABlAGwAbAA7ACQAdwBzAGgAZQBsAGwALgBBAHAAcABBAGMAdABpAHYAYQB0AGUAKAAiAEUAZABnAGUAIgApADsAJAB3AHMAaABlAGwAbAAuAFMAZQBuAGQASwBlAHkAcwAoACIAXgBtACIAKQA7AA==")
        
        # SOLUTION 3: Use nirsoft tool nircmd to mute Microsoft Edge. You need to be streaming in microsoft edge...lets be honest...you're not using it for anything else, so it's a great option since this will mute the entire browser and not individual tabs. 
        os.system("nircmd.exe muteappvolume \"msedge.exe\" 2")
        
    # Apple MacOS     
    if "darwin" in myPlatform:
        targetVol = 0

        # SOLUTION 1: Mute all audio. Not a great solution if listening to multiple things.
        '''if level == "mute":
            # This just mutes audio all together
            result = os.popen("osascript -e 'get volume settings'").read()
            outputVol = result.split(",")[0].split("output volume:")[1]
            savedSoundLevel = int(outputVol,10)
            #cmdStr = "osascript -e 'set volume output volume %s'"%(str(0))
            os.popen(cmdStr)
        elif level == "unmute":
            # This restores the audio to the previous volume.
            cmdStr = "osascript -e 'set volume output volume %s'"%(str(savedSoundLevel))
            os.popen(cmdStr)'''

        # SOLUTION 2: Mute audio per tab in Chrome. Good option if listening to multiple things, but will bring the stream window into focus when muting/unmuting...annoying.
        cmdStr = """osascript -e '
tell application "Google Chrome"
    activate
    repeat with w in (windows)
        set j to 0
        repeat with t in (tabs of w)
            set j to j + 1
            if URL of t contains "directv.com" then
                set (active tab index of w) to j
                set index of w to 1
                tell application "System Events" to tell process "Google Chrome"
                    perform action "AXRaise" of window 1
                    tell application "System Events" to click menu item "%s" of menu 1 of menu bar item "Tab" of menu bar 1 of application process "Chrome"
                end tell
                return
            end if
        end repeat
    end repeat
end tell'
    """%("Mute Site") # Mute site works to both mute and unmute the site
        os.popen(cmdStr)


        # SOLUTION 3: Mute specific tabs in Safari without having to bring the window into focus. Safari does not require the window to be in focus or to activate (note: the logo of the stream still needs to be visible). This will look at all safari windows open and check their tab URLs for the stream url (note: you stream needs to be in its own safari window and not in a window with multiple tabs). 
        # UPDATE: This is no longer an option in safari because you can not disable hardware acceleration...meaning the copyright protection through HDCP cannot be bypassed. 
        '''
        cmdStr = """osascript -e
try
    tell application "System Events"
        tell application "Safari"
            set winlist to every window
            set docItem to ""
            set tabName to ""
            repeat with win in winlist
                set tablist to every tab of win
                set foundTab to ""
                repeat with t in tablist
                    set urlStr to URL of t as string
                    set tName to name of t as string
                    if "%s" is in urlStr then
                        set docItem to win
                        set tabName to tName
                    end if
                end repeat
            end repeat
        end tell
        tell application process "Safari"
            tell window tabName
                --return get properties of button 3 of group 3 of toolbar 1
                try
                    tell button 3 of group 3 of toolbar 1
                        perform action "AXShowMenu"
                    end tell
                    if exists (menu item "Mute This Tab" of menu 1 of group 3 of toolbar 1) then
                        click menu item "Mute This Tab" of menu 1 of group 3 of toolbar 1
                    else if exists (menu item "Unmute This Tab" of menu 1 of group 3 of toolbar 1) then
                        click menu item "Unmute This Tab" of menu 1 of group 3 of toolbar 1
                    end if
                on error toolbarErrMsg
                    return "Error Level::Toggle Mute:" & space & toolbarErrMsg
                end try
                
            end tell
        end tell
    end tell
    do shell script "killall System\\ Events"
on error errmsg
    return "Error Level::Top:" & space & errmsg
end try
"""%("directv.com")
        os.popen(cmdStr)
        '''


#--------------------------------------------------------------
# Checking for subpicture inside larger picture
#
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def checkScreenshot(image,template):

    img_rgb = image #cv2.imread('big.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where( res >= threshold)
    
    # Sub image was not found, mute
    if len(loc[0]) == 0:
        return 0

    # Sub image was found, unmute
    elif len(loc[0]) > 0:
        return 1

        
# This detects text in an image, but requires tesseract (brew install tesseract, apt install tesseract, windows--look it up) as well as pip3 install pytesseract.
# It works ok, but for stylized logos like CNN it doesn't work great.
'''import cv2 
import numpy as np
import pytesseract
from PIL import Image

filename = 'big.png'
img = np.array(Image.open(filename))
norm_img = np.zeros((img.shape[0], img.shape[1]))
img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
img = cv2.GaussianBlur(img, (1, 1), 0)
text = pytesseract.image_to_string(img)

print(text)

if "live" in text.lower():
    print("yes")

quit()
'''   
    
#--------------------------------------------------------------
# Take screenshot in Microsoft Windows, Linux, and MacOS
#
from PIL import ImageGrab
def takeScreenshot():
    # To capture the screen
    image = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)#ImageGrab.grab()
    # To save the screenshot
    #image.save("big.png")
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    return image

#--------------------------------------------------------------
# Given an example of the logo (taken from a screenshot on your 
# screen from the stream)search for that logo at multiple 
# scales/resolutions until one matches.
#
def calibrate():
    image = cv2.imread("logo.png",0) #Image.open('logo.png')
    width = image.shape[1]
    height = image.shape[0] #image.size 

    template = ""

    images = [image]

    # Get a bunch of different resolutions for the logo
    while True:
        # Slowly down the image 5 percent at a time
        width  = round(width - (width * 0.05))
        height = round(height - (height * 0.05))

        # Too big
        if width > 300:
            continue
        # Too small
        elif width < 30 or height < 15:
            break

        print(width,height)
        tempImage = cv2.resize(image, (width, height)) #image.resize((width, height))
        images.append(tempImage)

    # Every few seconds take a screenshot and search for the the logo at different resolutions.
    while True:
        image = takeScreenshot()
        for template in images:
            
            found = checkScreenshot(image,template)
            if found == 1:
                width = template.shape[1]
                height = template.shape[0] 
                print("Template Found With Dimensions: %d,%d"%(width,height))
                return template
        print("Calibrating...Logo Not Found Yet...")
        time.sleep(2)


import time
from datetime import datetime

# Read in the logo.png and search for the logo at different resolutions until one is found.
template = calibrate()
muted = 0

while True:
    image = takeScreenshot()
    found = checkScreenshot(image,template)

    # Sub image was not found, mute
    if found == 0 and muted==0:
        print("Logo not found...muting...")
        controlSound("mute")
        muted = 1
    # Sub image was found, unmute
    elif found == 1 and muted==1:
        print("Logo found...unmuting...")
        controlSound("unmute")
        muted = 0

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    time.sleep(2)
