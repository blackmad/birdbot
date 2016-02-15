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
  bg_dir = os.path.dirname(os.path.realpath(__file__)) + '/' + 'backgrounds'
  bg_file = get_random_file(bg_dir)
  print bg_file
  bg = Image.open(bg_dir + '/' + bg_file)
  img.paste(bg, (0, 0))
 
  # calculate word size 
  word_fontfile = os.path.dirname(os.path.realpath(__file__)) + '/' + 'fonts/Times New Roman.ttf'
  print word_fontfile
  (word_font, word_size, word_width, word_height) = max_fontsize_for_box(draw, word_fontfile, word, width*0.625, height*0.25)

  # calculate definition size
  definition_lines = textwrap.wrap(definition, 40)
  wrapped_definition = '\n'.join(definition_lines)

  (definition_font, definition_size, definition_width, definition_height) = max_fontsize_for_box(
    draw, word_fontfile, wrapped_definition, width * 0.75, height * 0.5)

  definition_height_padding = height * 0.10
  total_height = word_height + definition_height + definition_height_padding

  # draw word we are defining
  word_x = (width - word_width) / 2
  word_y = (height - total_height) / 2
  draw.text((word_x, word_y), word, font=word_font, fill='black')
 
  # draw definition 
  definition_x = (width - definition_width) / 2
  definition_y = word_y + word_height + definition_height_padding
  draw.text((definition_x, definition_y), wrapped_definition, font=definition_font, fill='black')

  return img

import sys
def main():
  img = make(sys.argv[1], ' '.join(sys.argv[2:]))
  img.show()

if __name__ == "__main__":
  main() 
