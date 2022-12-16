# Discord-NOAA-image-Parser
## Welcome!
This bot will detect poor image quality NOAA satellite passes and delete/move these images

## Pre-requisites 
The first step is to create a discord application, and then a discord bot. (https://discord.com/developers/applications)
The variables in this such as name, PFP etc can be whatever you would like.
Please enable ALL Privileged Gateway Intents (there are 3 at time of writing) found under "Bot" tab.

I would reccomend installing GIT as this is the easiest way to install libraries. Otherwise these can be installed in any other means that suit.
If you don't have GIT installed already, look here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

As for required libraries, these are here with the correct git command to paste into your console.
| Library | GIT |
| ------ | ------ |
| discord | git install discord |
| numpy | git install numpy |
| PIL | git install Pillow |

## Getting-Started
1. Ensure all libraries are installed.
2. Using a text editor (please god not notepad) open bot.py. At the very top, you will see the following code to update. Nothing else needs to be changed, and the included comments should be pretty straight-forward:
```python
#===================================
# EDIT BELOW VARIABLES TO SETUP BOT:

TOKEN = 'DISCORD BOT TOKEN GOES HERE'

#Read is where the bot will LOOK for images. This channel must only be used for NOAA images as any other images will be parsed too
Read_Discord_Channel_ID = 123456
#Send is where the bot will send the file if it is poor quality. This is to ensure any false detections are still caught, and you will need to adjust the below thresholds.
# if Send_After_Detection is set to false, just set this to some random number. I.E: 123456
Send_Discord_Channel_ID = 123456

#set this to "False" if you do not want this bot to send the images in another chat after it detects a poor quality image.
# **WARNING** Setting this to false will mean the bot WILL just delete the image - for good.
# The good news is the image is not deleted from the original location it was sent from (Raspberry-Pi, Manually sent from Windows Desktop etc) so you won't lose that file.
Send_After_Detection = True

# If the mean is close to the maximum value (255 for 8-bit images) the image is considered clear 
# (not clear as in clarity. In this context clear = bad image).
# Default = 200
clear_threshold = 200

# Check if the image is static by comparing the standard deviation of the pixel values
# to a threshold value. If the standard deviation is below the threshold, the image is
# considered static.
# Default = 50
static_threshold = 50

#===================================

```
4. ENSURE all these files are in one folder if running on Windows for Batch script (Linux run: Python3 <PATH_TO_BOT.py>
3. There is an included batch file to run this bot, and a succesfull connection to your bot will look like this:
```
discord.client logging in using static token
discord.gateway Shard ID None has connected to Gateway (Session ID: #######################)
```
If you share your token anywhere on the internet, you will get an error like this below
```sh
discord.gateway Shard ID None session has been invalidated.
```
If this happens, please learn your lesson of not sharing this token anywhere, and generate a new one via https://discord.com/developers/applications


# Issues:
NONE!
Feel free to open an issue for anything (even just support) and i'll do my best to help
