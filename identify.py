#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from browser import get_browser
import sys
import re

MAINURL = """http://www.cnc.gov.ar/appnet/numeracion/geografica.aspx"""
REGEX = (r"""(?s)<tr[^>]*>[\s\n]*?"""
    """<td[^>]*?txtCuadroit[^>]*>(?:<[^>]*>)*(.*?)(?:<[^>]*>)*?</td>"""
    """.*?<td.*?>(?:<[^>]*>)*(.*?)(?:<[^>]*>)*?</td>.*?</tr>""")

def identify(codarea, numerolocal):
    browser = get_browser()
    form = browser.get_forms(MAINURL)[0]
    form["txt_indicativo"] = codarea
    form["txt_num_loc"] = numerolocal
    form.submit()
    for match in re.finditer(REGEX, browser.get_html()):
        print("%s: %s" % (match.group(1), match.group(2)))

def main():
    if len(sys.argv) == 3:
        return identify(sys.argv[1], sys.argv[2])
    else:
        print("Debe pasar como argumentos el código de área y el número:"
            "\n    e.g.: identify 387 4321321")
        return 1

if __name__ == "__main__":
    exit(main())
