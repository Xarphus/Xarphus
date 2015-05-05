#!/usr/bin/env python
#-*- coding:utf-8 -*-

def start_mdi():
        from files.modules_ui.ui_pp_mdi import Mdi_Main
        window = Mdi_Main()
        window.show_and_raise()
