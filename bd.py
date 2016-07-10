#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
file: bd.py $Id$
date: $Date$
"""

import sys

from lib.game import Juego, Ventana

def main():
    Ventana()
    juego = Juego()
    juego.menu()
    
if __name__ == "__main__":
    ret = main()
    sys.exit(ret)
    
