# https://github.com/exponential-decay/binary-numbers
#
# Application to automatically update a Twitter profile picture with a 
# dynamically created image. The code currently makes use of the Python 
# Imaging Library (PIL) to create dynamic images and then push them to 
# twitter daily.
#
# License: Beerware. For more information see GitHub repository:
# https://github.com/exponential-decay/binary-numbers/blob/master/license.md
# 
#
from twitter import *
import os
import base64
import random
import datetime
import StringIO
from PIL import Image

def HEXtoRGB(colorstring):
	#courtesy of code recipes. getrgb from PIL would be better (if it worked)
	colorstring = colorstring.strip()
	if colorstring[0] == '#': colorstring = colorstring[1:]
	r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
	r, g, b = [int(n, 16) for n in (r, g, b)]
	return (r, g, b)

def random_color():
	color_list = ['#4D4DFF', '#67C8FF', '#8D38C9', '#FF0000', '#FFFF00']
	random.seed()
	colorstr = color_list[random.randint(0, len(color_list)-1)]
	return HEXtoRGB(colorstr)
	
def create_image():

	binary_int_width = 5	#zeros needed
	xy_pixels = 30
	
	imgxy = xy_pixels * 7
		
	image = Image.new("RGB", (imgxy, imgxy))
	gx = 0
	
	s = bin(datetime.datetime.today().day).lstrip('-0b')
	bin_val = s.rjust(binary_int_width, '0')	#binary word

	gx = xy_pixels
	loop = 0
	
	for y in range(binary_int_width):	
		gy = xy_pixels
			
		color = random_color()
		for z in bin_val:
			if z == '0':
				gx+=0
				gy+=xy_pixels
			else:
				for gxx in range(xy_pixels):
					for gyy in range(xy_pixels):
						image.putpixel((gx+gxx, gy+gyy), color)
					
				gx+=0
				gy+=xy_pixels

		gx+=xy_pixels	#increment for each word

	output = StringIO.StringIO()
	image.save(output, "PNG")
	
	return output

def twitter_authentication():
	CONSUMER_KEYS = os.path.expanduser('.twitter-consumer-keys')
	CONSUMER_KEY, CONSUMER_SECRET = read_token_file(CONSUMER_KEYS)

	MY_TWITTER_CREDS = os.path.expanduser('.twitter-bin-numbers-credentials')
	if not os.path.exists(MY_TWITTER_CREDS):
		oauth_dance("binary-numbers", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

	oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
	twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
	
	return twitter

def update_profile_pic(twitter):
	output = create_image()
	profile_picture = base64.b64encode(output.getvalue())
	twitter.account.update_profile_image(image=profile_picture)
	
def main():
	twitter = twitter_authentication()
	update_profile_pic(twitter)

if __name__ == "__main__":
    main()