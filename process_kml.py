#! /usr/bin/env python
"""
Process an KML file downloaded from Google Maps Engine Lite and process it to
use on Maverick by:
- Download images and place then in a 'photo' directory
"""

from __future__ import absolute_import, print_function

import os
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


def main():
    """
    Main application
    """
    for filename in get_kml_files():
        doc = get_parsed_file(filename)

        for placemark in doc.Document.Folder.Placemark:
            try:
                print(placemark.name.text)
                print(placemark.ExtendedData.Data.value.text)
            except AttributeError:
                pass


main()
