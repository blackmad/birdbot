from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap

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

def max_fontsize_for_box(draw, fontfile, text, max_width, max_height):
  s = 100 
  w = max_width + 1
  h = max_height + 1

  print 'drawing %s' % text

  while w > max_width or h > max_height:
    font = ImageFont.truetype(fontfile, s)
    w, h = draw.textsize(text, font=font)
#    print 'at size %s, w: %s, h: %s' % (s, w, h)
    s -= 1

  return (font, s, w, h)

def make(word, definition):
  img = Image.new('RGBA', (width, height), (255, 255, 255, 255))
  draw = ImageDraw.Draw(img)

  # put down background
  bg_dir = 'backgrounds'
  bg_file = get_random_file(bg_dir)
  print bg_file
  bg = Image.open(bg_dir + '/' + bg_file)
  img.paste(bg, (0, 0))
  
  # draw word we are defining
  word_fontfile = 'fonts/Times New Roman.ttf'
  (word_font, word_size, word_width, word_height) = max_fontsize_for_box(draw, word_fontfile, word, width*0.625, height*0.25)
  
  word_width_padding = (width - word_width) / 2
  word_height_padding = height * 0.125
  draw.text((word_width_padding, word_height_padding), word, font=word_font, fill='black')
 
  # draw definition 
  definition_lines = textwrap.wrap(definition, 40)
  wrapped_definition = '\n'.join(definition_lines)

  (definition_font, definition_size, definition_width, definition_height) = max_fontsize_for_box(
    draw, word_fontfile, wrapped_definition, width * 0.75, height * 0.5)
  definition_width_padding = (width - definition_width) / 2
  definition_height_padding = word_height_padding + word_height + (height * 0.10)
  draw.text((definition_width_padding, definition_height_padding), wrapped_definition, font=definition_font, fill='black')

  return img

import sys
def main():
  img = make(sys.argv[1], ' '.join(sys.argv[2:]))
  img.show()

if __name__ == "__main__":
  main() 
