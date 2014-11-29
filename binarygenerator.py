import random
import datetime
import StringIO
from PIL import Image
from PIL import PngImagePlugin

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
	
	s = bin(int(get_date('day'))).lstrip('-0b')
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
	image.save(output, "PNG", pnginfo=write_metadata())
	return output

def get_date(purpose):	#tmp function for clarity
	
	date = datetime.datetime.today()	#TODO: Avoid repeat func() call, global?
	
	if purpose == 'fname':
		return date.strftime("%d-%m-%Y")
	elif purpose == 'title':
		return date.strftime("%d %B %Y")
	elif purpose == 'day':
		return date.strftime("%d")
	elif purpose == 'year':
		return date.strftime("%Y")

def write_metadata():

	meta = PngImagePlugin.PngInfo()
	meta.add_text("Title", get_date('title'))
	meta.add_text("Author", "Ross Spencer")
	meta.add_text("Copyright", "Creative Commons Attribution-ShareAlike 3.0 Unported License")
	meta.add_text("Software", "https://github.com/exponential-decay/binary-numbers")
	return meta
