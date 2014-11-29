import random
import datetime
import StringIO
import heritagepalette
import stripepatterns
from PIL import Image
from PIL import PngImagePlugin

class BinaryGenerator:

   def __init__(self):
      self.paletteno = self.getpalette()
      self.palettename = heritagepalette.NLNZ_PALETTE_RGB_VALUES[self.paletteno].keys()[0]

   def getpalette(self):
      return random.randint(0, len(heritagepalette.NLNZ_PALETTE_RGB_VALUES)-1)

   def random_color(self):
      color_list = heritagepalette.NLNZ_PALETTE_RGB_VALUES[self.paletteno].values()[0]
      random.seed()
      colorstr = color_list[random.randint(0, len(color_list)-1)]
      return self.HEXtoRGB(colorstr)

   def HEXtoRGB(self, colorstring):
      #courtesy of code recipes. getrgb from PIL would be better (if it worked)
      colorstring = colorstring.strip()
      if colorstring[0] == '#': colorstring = colorstring[1:]
      r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
      r, g, b = [int(n, 16) for n in (r, g, b)]
      return (r, g, b)

   def create_plain_image_matrix(self):
      
      pattern = stripepatterns.pattern_one_width
      hlen = len(pattern)
      hmax = max(pattern) 

      hborder = hlen + 2 #2black

      canvas = sum(pattern) + hborder
      space = sum(pattern)

      image = Image.new("RGB", (canvas, canvas))

      hxpos = hmax
      for p in pattern:
       
         color = self.random_color()

         for x in range(p):
            for y in range(space):
               image.putpixel((hxpos+x, hmax+y), color)

         hxpos = hxpos+p

      output = StringIO.StringIO()
      image.save(output, "PNG", pnginfo=self.write_metadata())
      return output

   def create_image(self):
      
      pattern = stripepatterns.pattern_one_width
      hlen = len(pattern)
      hmax = max(pattern) 

      hborder = hlen + 2 #2black

      canvas = sum(pattern) + hborder
      space = sum(pattern)

      image = Image.new("RGB", (canvas, canvas))

      binary_int_width = 5   #zeros needed
      s = bin(int(self.get_date('day'))).lstrip('-0b')
      bin_val = s.rjust(binary_int_width, '0')   #binary word

      negativeY = space/binary_int_width
      
      hxpos = hmax
      for p in pattern:
         color = self.random_color()
         for x in range(p):
            y = hmax  
            for val in bin_val:           
               for b in range(negativeY):
                  if val == '1':   
                     image.putpixel((hxpos+x, y+b), color)
               y = y + negativeY          
         hxpos = hxpos+p

      output = StringIO.StringIO()
      image.save(output, "PNG", pnginfo=self.write_metadata(self.palettename))
      return output

   #original creation routine...
   def _create_image_(self):

      binary_int_width = 5   #zeros needed
      xy_pixels = 30
      
      imgxy = xy_pixels * 7
         
      image = Image.new("RGB", (imgxy, imgxy))
      gx = 0
      
      s = bin(int(self.get_date('day'))).lstrip('-0b')
      bin_val = s.rjust(binary_int_width, '0')   #binary word

      gx = xy_pixels
      
      for y in range(binary_int_width):   
         gy = xy_pixels
            
         color = self.random_color()
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

         gx+=xy_pixels   #increment for each word

      output = StringIO.StringIO()
      image.save(output, "PNG", pnginfo=self.write_metadata())
      return output

   def get_date(self, purpose):   #tmp function for clarity
      
      date = datetime.datetime.today()   #TODO: Avoid repeat func() call, global?
      
      if purpose == 'fname':
         return date.strftime("%d-%m-%Y")
      elif purpose == 'title':
         return date.strftime("%d %B %Y")
      elif purpose == 'day':
         return date.strftime("%d")
      elif purpose == 'year':
         return date.strftime("%Y")

   def write_metadata(self, palette=False):

      meta = PngImagePlugin.PngInfo()
      meta.add_text("Title", self.get_date('title'))
      meta.add_text("Author", "Ross Spencer")
      meta.add_text("Copyright", "Creative Commons Attribution-ShareAlike 3.0 Unported License")
      meta.add_text("Software", "https://github.com/exponential-decay/binary-numbers")
      if palette != False:
         meta.add_text("Palette", palette)
      return meta
