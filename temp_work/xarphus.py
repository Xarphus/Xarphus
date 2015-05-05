#!/usr/bin/env python
#-*- coding:utf-8 -*-
FILE_NAME = "xarphus.py"
try:
    import sys
    import os
    from files.modStart import start_mdi
    print FILE_NAME + ": all modules are imported"
except IOError as (errno, strerror):
    print FILE_NAME + ": I/O error({0}): {1}".format(errno, strerror)
except:
    print FILE_NAME + ": Unexpected error:", sys.exc_info()[0]
    raise

def main():
    start_mdi()

if __name__ == "__main__":
    main()
