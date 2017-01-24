# -*- coding: utf-8 -*-

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
    sorted_list = sorted(os.listdir(dir), reverse=True)
    for filename in sorted_list:
        file = dir + filename

        #meta source: http://blog.client9.com/2007/08/28/python-pil-and-png-metadata-take-2.html
        im2 = Image.open(dir + filename)

        if 'Title' and 'Palette' in im2.info:
            tags += "<figure style='display:inline-block;'>"
            tags += "<img style='margin: 0; padding: 0;' src='" + imgdir + filename + "' title='" + im2.info['Title'] + "' alt='" + im2.info['Title'] + "' height='210' width='210' />" + "\n\t\t\t"
            tags += "<figcaption style='background-color: #110000;'>"
            tags += "<table style='border-collapse: collapse; width: 210px;'>"
            tags += "<tr>"
            tags += "<td 'width=60px'>" + "<b>Title</b>" + "</td><td 'width=150px'>" + im2.info['Title'] + "</td>"
            tags += "</tr><tr>"
            tags += "<td 'width=60px'>" + "<b>Palette</b>" + "</td><td 'width=150px'>" + im2.info['Palette'] + "</td>"
            tags += "</tr>"
            tags += "</table></figcaption></figure>"
            #tags += "\n\t\t\t"

    return tags

def web_page():
    header = """<!DOCTYPE html>
    	<html lang="en-gb">
    		<head>
    			<meta charset="utf-8"/>
                <meta name="author" content="Ross Spencer">
                <meta name="description" content="Output of work to automatically update my twitter profile picture with dynamic content, code here: https://github.com/exponential-decay/binary-numbers">
    			<title>binary-numbers by exponentialdecay.co.uk</title>
    		</head>
    		<body style="background-color: #110000; font-family: arial, verdana; font-size: 10px; color:white;">
    		<h1 style="font-size: 10px; color:white;"><b>Binary Numbers:</b> A project by <a style="font-size: 10px; color:white;" href="https://twitter.com/beet_keeper?lang=en">@beet_keeper</a></h1>
    		<h2 style="font-size: 10px; color:white;"><b>Source Code:</b> <a style="font-size: 10px; color:white;" href="https://github.com/exponential-decay/binary-numbers">GitHub</a></h2>
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
