from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os 
import pythoncom
#? The pywin32 package is required for pythoncom 
#? HOWEVER, the pywin32 package can ONLY be installed on Windows
#? if you're developing on Linux this package wont install 
#? you will recieve an error if you try and: pip install pywin32
#? https://pypi.org/project/pywin32/
#? Source from package author - https://github.com/mhammond/pywin32/issues/1739

import pyWinhook 

import sys
import time

import win32clipboard