#!/usr/bin/env python
import os
import sys
import socket

if __name__ == "__main__":
    if socket.gethostname() == 'nsmsc.kr':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "choir.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "choir.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
