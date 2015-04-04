#! /usr/bin/env python
"""
Process an KML file downloaded from Google Maps Engine Lite and process it to
use on Maverick by:
- Download images and place then in a 'photo' directory
"""

from __future__ import absolute_import, print_function

import os
import urllib
from pykml import parser


def get_kml_files():
    """
    Return all KML files in the current directory
    """
    path = os.path.dirname(os.path.realpath(__file__))

    return [filename for filename in os.listdir(path)
            if filename[-4:].lower() == '.kml']


def get_parsed_file(filename):
    """
    Return a parsed file
    """
    return parser.parse(open(filename, 'r')).getroot()


def check_for_dir(path):
    """
    Check  if the given path exists, otherwise, create it
    """
    if not os.path.exists(path):
        os.makedirs(path)


def download_pic(url, img_name, dest_dir='photos'):
    """
    Download an image from the given url and store it on the specified dir
    """
    if ' ' in url:
        url = url.split(' ')[0]

    if '?' in url:
        # Lets assume it's 'jpg'
        extension = 'jpg'
    else:
        extension = url.split('.')[-1]

    filename = '{0}.{1}'.format(img_name.encode('utf8'), extension)
    filename = os.path.join(dest_dir, filename)

    # If the file already exists, don't download it again
    if not os.path.isfile((filename)):
        print('Downloading: {0}'.format(url))
        urllib.urlretrieve(url, filename)


def main():
    """
    Main application
    """
    check_for_dir('photos')

    for filename in get_kml_files():
        doc = get_parsed_file(filename)

        print('Downloading pictures for {0}'.format(filename))

        for placemark in doc.Document.Folder.Placemark:
            try:
                name = placemark.name.text
                url = placemark.ExtendedData.Data.value.text

                print('{0}'.format(name.encode('utf8')))
                download_pic(url, name)
            except AttributeError:
                pass


main()
