# complimentary script to binary-numbers.py
#
# reads images directory on pythonanywhere.com and outputs a grid of
# the images it finds as a temporary gallery placeholder for the 
# images created until some sort of gallery upload utility is available.
#
# License: Beerware. For more information see GitHub repository:
# https://github.com/exponential-decay/binary-numbers/blob/master/license.md
# 
#
import os
import datetime
from PIL import Image
from PIL import PngImagePlugin

import web
urls = (
  '/', 'index'
)

# comment out these two lines if you want to use another framework
app = web.application(urls, globals())
application = app.wsgifunc()

dir = '/var/www/static/images/'  #dir to read
imgdir = 'images/' #dir to display

def img_tags():
    tags = ''
    for filename in os.listdir(dir):
        file = dir + filename
        im2 = Image.open(dir + filename)
        tags += "<img src='" + imgdir + filename + "' alt='" + im2.info['Title'] + "' height='210' width='210' />" + "\n\t\t\t"
    return tags

def web_page():
    header = """<!DOCTYPE html>
    	<html lang="en-gb">
    		<head>
    			<meta charset="utf-8"/>
    			<link rel="stylesheet" href="css/x.css">
    			<title>binary-primes calendar by exponentialdecay.co.uk</title>
    		</head>
    		<body>
    			"""

    footer = 	"""
    		</body>
    	</html>
    			"""

    web_page = header + img_tags() + footer
    return web_page

class index:
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        mypage = web_page()
        return mypage
