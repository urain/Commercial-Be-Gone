# Commercial-Be-Gone
Mutes audio when a commercial is detected.

## DESCRIPTION: 
While streaming news for example, this program can automatically mute audio when it detects that commercials are playing i.e. While watching CNN, Fox, etc; the news logo is always visible while the program is active. However, when it cuts to commercial the logo disappears.

## MACOS:
Confirmed working for MacOS using Google Chrome

sudo pip3 install comtypes opencv-python numpy matplotlib Pillow

## WINDOWS:
Confirmed working for Microsoft Windows using Microsoft Edge.

pip3 install pycaw comtypes opencv-python numpy matplotlib Pillow

## LINUX:
Haven't implemented a solution yet.

## NOTE: 
You need to disable Hardware Acceleration in Google Chrome (MacOS) or Microsoft Edge (Windows) for HDCP copyright protection to allow screenshots to capture a still image of the streaming service, in this case CNN News Stream. Otherwise your secreenshots will be black if your video device and HDMI cable support HDCP and the service you are streaming has HDCP copyright protection enabled.

## NOTE: 
You need to take a cropped snapshot of the logo you want, rename it to logo.png, and place it in the program folder.

## NOTE: 
The logo for the news channel needs to be visible on the screen somewhere i.e. if you were to take a screenshot you would need to be able to find it with your own eyes.

