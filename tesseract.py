###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os
import sys
import subprocess
import tempfile

import ImageFile
import Image
import TiffImagePlugin

IMAGE_SUFFIX = ".tif"
TEXT_SUFFIX = ".txt"

class Tesseract:
    """"""
    def __init__(self, data, filter=None):
        """"""
        self.tesseract = "tesseract"
        self.text = tempfile.NamedTemporaryFile(suffix=TEXT_SUFFIX)
        self.image = tempfile.NamedTemporaryFile(suffix=IMAGE_SUFFIX)
        self.image_name = self.image.name
        self.text_name = self.text.name.rsplit(TEXT_SUFFIX, 1)[0]
        p = ImageFile.Parser()
        p.feed(data)
        if filter:
            image = filter(p.close())
        else:
            image = p.close()
        image.save(self.image_name)

    def get_captcha(self):
        """"""
        captcha = ""
        if subprocess.call([self.tesseract, self.image_name, self.text_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
            captcha = self.text.file.readline().strip()
        self.text.file.close()
        self.image.file.close()
        return captcha

if __name__ == "__main__":
    f = file(sys.argv[1], "r")
    t = Tesseract(f.read())
    print t.get_captcha()
