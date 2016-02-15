from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import cairo
import cairo_font
import io

import os
import random

height = 220
width = 440

def get_random_file(path):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(path)
  index = random.randrange(0, len(files))
  return files[index]

def max_fontsize_for_box(cr, fontname, text, max_width, max_height):
  s = 100 
  w = max_width + 1
  h = max_height + 1

  print 'drawing %s' % text

  cr.select_font_face(fontname, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

  while w > max_width or h > max_height:
    cr.set_font_size(s)
    (x, y, w, h, dx, dy) = cr.text_extents(text)
    print 'at size %s, w: %s, h: %s' % (s, w, h)
    s -= 1

  return (s, w, h)

def make(word, definition):
  surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
  cr = cairo.Context(surface)

  # put down background
  bg_dir = 'backgrounds'
  bg_file = get_random_file(bg_dir)
  print bg_file
  i = io.BytesIO(open(bg_dir + '/' + bg_file).read())
  im = Image.open(i)
  imagebuffer = io.BytesIO()  
  im.save(imagebuffer, format="PNG")
  imagebuffer.seek(0)
  imagesurface = cairo.ImageSurface.create_from_png(imagebuffer)

  cr.save()
  cr.set_source_surface(imagesurface, 0, 0)
  cr.paint()
  cr.restore()

  fontname = "Times New Roman"
  fo = cairo.FontOptions()
  fo.set_antialias(cairo.ANTIALIAS_DEFAULT)
  fo.set_hint_style(5)
  cr.set_font_options(fo)  

 
  # calculate word size 
  (word_size, word_width, word_height) = max_fontsize_for_box(cr, fontname, word, width*0.625, height*0.25)

  # calculate definition size
  definition_lines = textwrap.wrap(definition, 40)
  wrapped_definition = '\n'.join(definition_lines)

  (definition_size, definition_width, definition_height) = max_fontsize_for_box(
    cr, fontname, wrapped_definition, width * 0.75, height * 0.5)

  definition_height_padding = height * 0.10
  total_height = word_height + definition_height + definition_height_padding

  # draw word we are defining
  word_x = (width - word_width) / 2
  word_y = (height - total_height) / 2
  cr.save()
  cr.move_to(word_x, word_y)
  cr.show_text(word)
  cr.restore()
 
  # draw definition 
  definition_x = (width - definition_width) / 2
  definition_y = word_y + word_height + definition_height_padding
  cr.move_to(definition_x, definition_y)
  cr.show_text(wrapped_definition)

  img = Image.frombuffer(
    'RGBA', (surface.get_width(),
             surface.get_height()),
             surface.get_data(), 'raw', 'BGRA', 0, 1)
  return img

import sys
def main():
  img = make(sys.argv[1], ' '.join(sys.argv[2:]))
  img.show()

if __name__ == "__main__":
  main() 
