#!/usr/bin/python

import sys
import os
from PIL import Image
import json
import argparse

def generateIOSAppIcon(source, base_size, scale, output_dir, device, app_contents):
  if os.path.exists(output_dir) == False:
    print '-> Output directory not exists. Create new: ' + output_dir;
    os.makedirs(output_dir)

  file_name = os.path.basename(source)
  file_name_parts = file_name.split('.')

  save_template = '{0}/{1}-{2}x{2}@{3}x.{4}'
  size_scaled = int(base_size * scale)
  save_path = save_template.format(output_dir, file_name_parts[0], base_size, scale, file_name_parts[1])

  if os.path.exists(save_path) == True:
    app_contents['images'].append({
      "idiom": device,
      "size": "{0}x{0}".format(base_size),
      "scale": "{0}x".format(scale),
      "filename": os.path.basename(save_path)
    });

    return

  with open(source, 'r+b') as f:
    with Image.open(f) as image:
      base_image = Image.new('RGBA', (size_scaled, size_scaled), color='white')

      new_image = image.resize((size_scaled, size_scaled), Image.ANTIALIAS)
      base_image.paste(new_image, (0, 0))

      base_image.save(save_path, format='png', quality=100)
      app_contents['images'].append({
        "idiom": device,
        "size": "{0}x{0}".format(base_size),
        "scale": "{0}x".format(scale),
        "filename": os.path.basename(save_path)
      })
      print "  -> Generated icon: " + save_path

      new_image.close()
      base_image.close()
      image.close()
    f.close()

def generateItunesAtWorkIcon(source, size, scale, output_dir):
  size_scaled = size * scale
  save_path = '{0}/iTunesArtwork@{1}x.png'.format(output_dir, scale)

  with open(source, 'r+b') as f:
    with Image.open(f) as image:
      new_image = image.resize((size_scaled, size_scaled), Image.ANTIALIAS)
      
      base_image = Image.new(new_image.mode, (size_scaled, size_scaled), 'black')
      base_image = Image.alpha_composite(base_image, new_image)

      base_image.save(save_path, format='png', quality=100)

      print '  -> Generated iTunesArtwork icon: ' + save_path

      base_image.close()
      new_image.close()
      image.close()      
    f.close()

def generateAndroidLauncherIcon(source, size, output_dir, name='ic_launcher'):
  if os.path.exists(output_dir) == False:
    print '-> Output directory not exists. Create new: ' + output_dir;
    os.makedirs(output_dir)

  save_path = '{0}/{1}.png'.format(output_dir, name)

  with open(source) as f:
    with Image.open(f) as image:
      base_image = Image.new('RGBA', (size, size), color='white')

      new_image = image.resize((size, size), Image.ANTIALIAS)
      base_image.paste(new_image, (0, 0))

      base_image.save(save_path, format='png', quality=100)
      print "  -> Generated icon: " + save_path

      new_image.close()
      base_image.close()
      image.close()

    f.close()

def main():
  parser = argparse.ArgumentParser(description='Generate icons for App Store and Play Store')
  parser.add_argument('-i', '--input', help='Path to input source')
  parser.add_argument('-o', '--output', help='Path to output icons')

  args = parser.parse_args()
  
  source = args.input
  if os.path.exists(source) == False:
    print ' > ' + source + ' not exists';
    sys.exit()

  file_name_parts = os.path.basename(source).split('.')
  if file_name_parts[1] != 'png':
    print ' > Only support PNG image'
    sys.exit()


  output_dir = args.output + '/AppIcons'
  
  app_icon_contents = {
    'images': [],
    'info': {
      'version': 1
    }
  }
  
  # iphone
  generateIOSAppIcon(source, 60, 2, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 60, 3, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)

  generateIOSAppIcon(source, 40, 3, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 40, 2, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 29, 3, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 29, 2, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 20, 3, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  generateIOSAppIcon(source, 20, 2, output_dir + '/ios/AppIcon.appiconset', 'iphone', app_icon_contents)
  
  # ipad
  generateIOSAppIcon(source, 83.5, 2, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 76, 2, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 76, 1, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 40, 2, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 40, 1, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 29, 2, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 29, 1, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 20, 2, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)
  generateIOSAppIcon(source, 20, 1, output_dir + '/ios/AppIcon.appiconset', 'ipad', app_icon_contents)

  generateItunesAtWorkIcon(source, 1024, 1, output_dir + '/ios/AppIcon.appiconset')
  app_icon_contents['images'].append({
    "idiom": 'ios-marketing',
    "size": "1024x1024",
    "scale": "1x",
    "filename": 'iTunesArtwork@1x.png'
  });

  with open (output_dir + '/ios/AppIcon.appiconset/Contents.json', 'w+') as output_file:
    json.dump(app_icon_contents, output_file, indent=2)
    output_file.close()

  # iTunes at work
  generateItunesAtWorkIcon(source, 512, 1, output_dir + '/ios')
  generateItunesAtWorkIcon(source, 512, 2, output_dir + '/ios')
  generateItunesAtWorkIcon(source, 512, 3, output_dir + '/ios')

  # android launcher icons
  generateAndroidLauncherIcon(source, 48, output_dir + '/android/mipmap-mdpi')
  generateAndroidLauncherIcon(source, 72, output_dir + '/android/mipmap-hdpi')
  generateAndroidLauncherIcon(source, 96, output_dir + '/android/mipmap-xhdpi')
  generateAndroidLauncherIcon(source, 144, output_dir + '/android/mipmap-xxhdpi')
  generateAndroidLauncherIcon(source, 192, output_dir + '/android/mipmap-xxxhdpi')
  generateAndroidLauncherIcon(source, 512, output_dir + '/android', 'playstore-icon')

if __name__ == '__main__':
  main()
