import discord
from discord.ext import commands
import requests
from PIL import Image
import numpy as np
from io import BytesIO

global Read_Discord_Channel_ID, Send_Discord_Channel_ID, static_threshold, clear_threshold, Send_After_Detection

# This bot was created for use with the raspberry-noaa-v2, which automatically sends decoded images in discord. Occasionally you will get a poor image, in which clogs up the discord channel.
# This bot waits for an image to be sent in a SPECIFIC channel, parses it to check its quality, and can either
# A: Essentially "Move" the image to another channel. I.e "Trash-Sat-Images"
# B: Completely delete it outright (only deletes it from discord)

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

# This will remove small resolution images
MIN_WIDTH = 750
MIN_HEIGHT = 500

#===================================

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!',intents=intents)

client = discord.Client(intents=intents)

def is_poor_quality_noaa_satellite_image(image):
    print("PARSING...")
    # Convert the image to a NumPy array
    image_array = np.array(image)
    
    # get the resolution of image
    width, height = image.size


    #First check is resolution, if smaller than set minmums, considered poor quality.
    if width > MIN_WIDTH or height < MIN_HEIGHT:
        print("Image parsed - FAILED resolution test           image res values (W x H): ", width, ",", height)
        print(" ")
        return True
    # Check if the image is static by comparing the standard deviation of the pixel values
    # to a threshold value. If the standard deviation is below the threshold, the image is
    # considered static.
    if image_array.std() < static_threshold:
        print("Image parsed - FAILED static test           image STD value: ", image_array.std())
        print(" ")
        return True

    # You can also check if the image is clear by checking the mean pixel value. If the mean
    # is close to the maximum value (255 for 8-bit images), the image is considered clear.
    if image_array.mean() > clear_threshold:
        print("Image parsed - FAILED clarity test           image mean value: ", image_array.mean())
        print(" ")
        return True

    # If the image is neither static nor clear, it is considered good quality
    print("Image parsed - considered good quality!       image mean value: ", image_array.mean(),"         image std value: ", image_array.std())
    print(" ")
        
    return False

@client.event
async def on_message(message):
    # Make sure the message is from a channel and not from a DM
    if message.guild:
        # Make sure the message is from the target channel
        if message.channel.id == Read_Discord_Channel_ID:  # Replace with the actual channel ID
            # Make sure the message is an image attachment
            if message.attachments:
                attachment = message.attachments[0]
                # Check if the attachment is a PNG image
                if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.png'):
                    # Download the image and open it using the Pillow library
                    image_data = requests.get(attachment.url).content
                    image = Image.open(BytesIO(image_data))

                    # Check if the image is a poor quality NOAA satellite image
                    if is_poor_quality_noaa_satellite_image(image):
                        # Find the target channel where you want to copy the image
                        target_channel_id = Send_Discord_Channel_ID  # Replace with the actual channel ID
                        target_channel = client.get_channel(target_channel_id)

                        # Send the image to the target channel
                        await target_channel.send(file=discord.File(BytesIO(image_data), filename=attachment.filename))

                        # Delete the original message from the source channel
                        await message.delete()

client.run(TOKEN)