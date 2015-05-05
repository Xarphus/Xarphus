#!/usr/bin/env python
#-*- coding:utf-8 -*-

FILE_NAME = "xarphus.py"
try:
    import sys
    import os
    print FILE_NAME + ": all modules are imported"
except IOError as (errno, strerror):
    print FILE_NAME + ": I/O error({0}): {1}".format(errno, strerror)
except:
    print FILE_NAME + ": Unexpected error:", sys.exc_info()[0]
    raise

def main():
    from src.ui_pp_mdi import MDI_Window
    window = MDI_Window()
    window.show_and_raise()

if __name__ == "__main__":
    main()
