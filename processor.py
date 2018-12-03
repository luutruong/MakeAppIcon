#!/usr/bin/python

import sys
from termcolor import colored
import os
from PIL import Image
import json

def generateAppStoreIcons(file_path, size, output, contents):
  if os.path.exists(output) == False:
    print colored('-> Output directory not exists. Create new: ' + output);
    os.makedirs(output)

  file_name = os.path.basename(file_path)
  file_name_parts = file_name.split('.')

  save_template = '{0}/{1}-{2}x{2}@{3}x.{4}'

  scale_sizes = [1, 2, 3]
  for scale_size in scale_sizes:
    size_scaled = size * scale_size
    save_path = save_template.format(output, file_name_parts[0], size, scale_size, file_name_parts[1])

    with open(file_path, 'r+b') as f:
      with Image.open(f) as image:
        base_image = Image.new('RGBA', (size_scaled, size_scaled), color='white')

        new_image = image.resize((size_scaled, size_scaled), Image.ANTIALIAS)
        base_image.paste(new_image, (0, 0))

        base_image.save(save_path, format='png', quality=100)
        contents['images'].append({
          "idiom": "ipad",
          "size": "{0}x{0}".format(size_scaled),
          "scale": "{0}x".format(scale_size),
          "filename": os.path.basename(save_path)
        })
        print colored("  -> Generated icon: " + save_path, 'green')
    f.close()

def main():
  if len(sys.argv) < 2:
    print colored(" > Invalid command.\nMust be run `python maker.py /path/to/image`", 'red')
    sys.exit()

  source = sys.argv[1]
  if os.path.exists(source) == False:
    print colored(' > ' + source, 'red') + colored(' not exists');
    sys.exit()

  output_dir = './results'
  
  app_store_icon_sizes = [20, 29, 40, 50, 57, 60, 72, 76]
  app_icon_contents = {
    'images': [],
    'info': {
      'version': 1
    }
  }
  for app_store_icon_size in app_store_icon_sizes:
    generateAppStoreIcons(source, app_store_icon_size, output_dir + '/AppIcon.appiconset', app_icon_contents)

  with open (output_dir + '/AppIcon.appiconset/Contents.json', 'w+') as output_file:
    json.dump(app_icon_contents, output_file, indent=2)
  output_file.close()

if __name__ == '__main__':
  main()
