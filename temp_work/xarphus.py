#!/usr/bin/env python
#-*- coding:utf-8 -*-
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

#!/usr/bin/env python
#-*- coding:utf-8 -*-

def main():
        from files.modules_ui.ui_pp_mdi import Mdi_Main
        window = Mdi_Main()
        window.show_and_raise()

if __name__ == "__main__":
    main()
