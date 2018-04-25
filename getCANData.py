import can
import time
import queue
import logging
import models
import collections

import sys
import random
import ui

import serial

from PyQt5 import QtCore, QtWidgets
from screenwrite import *

from errorList import *
from configList import *

from math import pi
from decimal import *
from datetime import *

# initialization of serial port
portName = '/dev/ttyACM0'
baudRate = 115200

# byte arrays output of dashboard display key presses (press and depress)
up    = b'\x80\x01\x01q\xc2\x80\x01\x07G\xa7'
down  = b'\x80\x01\x02\xea\xf0\x80\x01\x08\xb0_'
left  = b'\x80\x01\x03c\xe1\x80\x01\t9N'
right = b'\x80\x01\x04\xdc\x95\x80\x01\n\xa2|'
check = b'\x80\x01\x05U\x84\x80\x01\x0b+m'
close = b'\x80\x01\x06\xce\xb6\x80\x01\x0c\x94\x19'

_pollFrequency = 3.0
#global time counter
_time = 0

class Datapoint(object):

	def __init__(self):
		sensor_id = 0
		sensor_name = ""
		count = 0
		byte_length = 0
		data = 0
		system = ""
		scalar = 1
		sampleTime = 15
		pack = None

listOfViewableData = [{"address": 0x100, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":1, "description": "State"},
					  {"address": 0x100, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":2, "description": "Voltage"},
					  {"address": 0x100, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 1,  "updated": 0, "id":3, "description": "Current"},
					  {"address": 0x100, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":4, "description": "SOC"},
					  {"address": 0x101, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":5, "description": "Columbs"},

					  {"address": 0x101, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":6, "description": "Cell 1 Status"},
					  {"address": 0x101, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":7, "description": "Cell 2 Status"},
					  {"address": 0x101, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":8, "description": "Cell 3 Status"},
					  {"address": 0x101, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":9, "description": "Cell 4 Status"},
					  {"address": 0x102, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":10, "description": "Cell 5 Status"},
					  {"address": 0x102, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":11, "description": "Cell 6 Status"},
					  {"address": 0x102, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":12, "description": "Cell 7 Status"},

					  {"address": 0x102, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":13, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":14, "description": "Cell 2 Voltage"},
					  {"address": 0x103, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":15, "description": "Cell 3 Voltage"},
					  {"address": 0x103, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":16, "description": "Cell 4 Voltage"},
					  {"address": 0x103, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":17, "description": "Cell 5 Voltage"},
					  {"address": 0x103, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":18, "description": "Cell 6 Voltage"},
					  {"address": 0x104, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":19, "description": "Cell 7 Voltage"},

					  {"address": 0x104, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":20, "description": "Cell 1 Temp"},
					  {"address": 0x104, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":21, "description": "Cell 2 Temp"},
					  {"address": 0x104, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":22, "description": "Cell 3 Temp"},
					  {"address": 0x105, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":23, "description": "Cell 4 Temp"},
					  {"address": 0x105, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":24, "description": "Cell 5 Temp"},
					  {"address": 0x105, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":25, "description": "Cell 6 Temp"},
					  {"address": 0x105, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":26, "description": "Cell 7 Temp"},


					  {"address": 0x200, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":27, "description": "State"},
					  {"address": 0x200, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":28, "description": "Voltage"},
					  {"address": 0x200, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 1,  "updated": 0, "id":29, "description": "Current"},
					  {"address": 0x200, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":30, "description": "SOC"},
					  {"address": 0x201, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":31, "description": "Columbs"},

					  {"address": 0x201, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":32, "description": "Cell 1 Status"},
					  {"address": 0x201, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":33, "description": "Cell 2 Status"},
					  {"address": 0x201, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":34, "description": "Cell 3 Status"},
					  {"address": 0x201, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":35, "description": "Cell 4 Status"},
					  {"address": 0x202, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":36, "description": "Cell 5 Status"},
					  {"address": 0x202, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":37, "description": "Cell 6 Status"},
					  {"address": 0x202, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":38, "description": "Cell 7 Status"},

					  {"address": 0x202, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":39, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":40, "description": "Cell 2 Voltage"},
					  {"address": 0x203, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":41, "description": "Cell 3 Voltage"},
					  {"address": 0x203, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":42, "description": "Cell 4 Voltage"},
					  {"address": 0x203, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":43, "description": "Cell 5 Voltage"},
					  {"address": 0x203, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":44, "description": "Cell 6 Voltage"},
					  {"address": 0x204, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":45, "description": "Cell 7 Voltage"},

					  {"address": 0x204, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":46, "description": "Cell 1 Temp"},
					  {"address": 0x204, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":47, "description": "Cell 2 Temp"},
					  {"address": 0x204, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":48, "description": "Cell 3 Temp"},
					  {"address": 0x205, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":49, "description": "Cell 4 Temp"},
					  {"address": 0x205, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":50, "description": "Cell 5 Temp"},
					  {"address": 0x205, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":51, "description": "Cell 6 Temp"},
					  {"address": 0x205, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":52, "description": "Cell 7 Temp"},


					  {"address": 0x300, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":53, "description": "State"},
					  {"address": 0x300, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":54, "description": "Voltage"},
					  {"address": 0x300, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 1,  "updated": 0, "id":55, "description": "Current"},
					  {"address": 0x300, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":56, "description": "SOC"},
					  {"address": 0x301, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":57, "description": "Columbs"},

					  {"address": 0x301, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":58, "description": "Cell 1 Status"},
					  {"address": 0x301, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":59, "description": "Cell 2 Status"},
					  {"address": 0x301, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":60, "description": "Cell 3 Status"},
					  {"address": 0x301, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":61, "description": "Cell 4 Status"},
					  {"address": 0x302, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":62, "description": "Cell 5 Status"},
					  {"address": 0x302, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":63, "description": "Cell 6 Status"},
					  {"address": 0x302, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":64, "description": "Cell 7 Status"},

					  {"address": 0x302, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":65, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":66, "description": "Cell 2 Voltage"},
					  {"address": 0x303, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":67, "description": "Cell 3 Voltage"},
					  {"address": 0x303, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":68, "description": "Cell 4 Voltage"},
					  {"address": 0x303, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":69, "description": "Cell 5 Voltage"},
					  {"address": 0x303, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":70, "description": "Cell 6 Voltage"},
					  {"address": 0x304, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":71, "description": "Cell 7 Voltage"},

					  {"address": 0x304, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":72, "description": "Cell 1 Temp"},
					  {"address": 0x304, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":73, "description": "Cell 2 Temp"},
					  {"address": 0x304, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":74, "description": "Cell 3 Temp"},
					  {"address": 0x305, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":75, "description": "Cell 4 Temp"},
					  {"address": 0x305, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":76, "description": "Cell 5 Temp"},
					  {"address": 0x305, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":77, "description": "Cell 6 Temp"},
					  {"address": 0x305, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":78, "description": "Cell 7 Temp"},


					  {"address": 0x400, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":79, "description": "State"},
					  {"address": 0x400, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":80, "description": "Voltage"},
					  {"address": 0x400, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 1,  "updated": 0, "id":81, "description": "Current"},
					  {"address": 0x400, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":82, "description": "SOC"},
					  {"address": 0x401, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":83, "description": "Columbs"},

					  {"address": 0x401, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":84, "description": "Cell 1 Status"},
					  {"address": 0x401, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":85, "description": "Cell 2 Status"},
					  {"address": 0x401, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":86, "description": "Cell 3 Status"},
					  {"address": 0x401, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":87, "description": "Cell 4 Status"},
					  {"address": 0x402, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":88, "description": "Cell 5 Status"},
					  {"address": 0x402, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":89, "description": "Cell 6 Status"},
					  {"address": 0x402, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":90, "description": "Cell 7 Status"},

					  {"address": 0x402, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":91, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":92, "description": "Cell 2 Voltage"},
					  {"address": 0x403, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":93, "description": "Cell 3 Voltage"},
					  {"address": 0x403, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":94, "description": "Cell 4 Voltage"},
					  {"address": 0x403, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":95, "description": "Cell 5 Voltage"},
					  {"address": 0x403, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":96, "description": "Cell 6 Voltage"},
					  {"address": 0x404, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 15, "updated": 0, "id":97, "description": "Cell 7 Voltage"},

					  {"address": 0x404, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":98, "description": "Cell 1 Temp"},
					  {"address": 0x404, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":99, "description": "Cell 2 Temp"},
					  {"address": 0x404, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":100, "description": "Cell 3 Temp"},
					  {"address": 0x405, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":101, "description": "Cell 4 Temp"},
					  {"address": 0x405, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":102, "description": "Cell 5 Temp"},
					  {"address": 0x405, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":103, "description": "Cell 6 Temp"},
					  {"address": 0x405, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":104, "description": "Cell 7 Temp"},


					  {"address": 0x601, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 1,  "updated": 0, "id":105, "description": "Motor RPM"},
					  {"address": 0x601, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":106, "description": "Motor Temp"},
					  {"address": 0x601, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":107, "description": "Controller Temp"},
					  {"address": 0x601, "offset": 4, "byteLength": 2, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 1,  "updated": 0, "id":108, "description": "RMS Current"},
					  {"address": 0x601, "offset": 6, "byteLength": 2, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 5,  "updated": 0, "id":109, "description": "Capacitor Voltage"},
					  {"address": 0x602, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 30, "updated": 0, "id":110, "description": "Stator Frequency"},
					  {"address": 0x602, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":111, "description": "Controller Fault Primary"},
					  {"address": 0x602, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":112, "description": "Controller Fault Secondary"},
					  {"address": 0x602, "offset": 4, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 1,  "updated": 0, "id":113, "description": "Throttle Input"},
					  {"address": 0x602, "offset": 5, "byteLength": 1, "system": "MC", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 1,  "updated": 0, "id":114, "description": "Brake Input"},


					  {"address": 0x0F2, "offset": 0, "byteLength": 1, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 5,  "updated": 0, "id":115, "description": "TSI State"},
					  {"address": 0x0F2, "offset": 1, "byteLength": 2, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":116, "description": "IMD"}, #IMD needs multiplied by 10
					  {"address": 0x0F2, "offset": 3, "byteLength": 2, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 100, "sampleTime": 5,  "updated": 0, "id":117, "description": "Throttle Voltage"}, #Needs multiplied by 10
					  {"address": 0x0F2, "offset": 5, "byteLength": 1, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 5,  "updated": 0, "id":118, "description": "Brake Press"}, #1 if pressed, 0 if not
					  {"address": 0x0F2, "offset": 6, "byteLength": 1, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 5,  "updated": 0, "id":119, "description": "AIRS Status"}, #1 if closed, 0 if open
					  {"address": 0x0F3, "offset": 0, "byteLength": 2, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 10, "sampleTime": 15, "updated": 0, "id":120, "description": "TSV Voltage"},
					  {"address": 0x0F3, "offset": 2, "byteLength": 2, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1000, "sampleTime": 1,  "updated": 0, "id":121, "description": "TSV Current"},
					  {"address": 0x0F3, "offset": 4, "byteLength": 2, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 15, "updated": 0, "id":122, "description": "TSI Temp"},
					  {"address": 0x0F3, "offset": 6, "byteLength": 1, "system": "TSI", "pack": 0, "count": 0, "data": 0, "displayValue": '-', "scalar": 1, "sampleTime": 5,  "updated": 0, "id":123, "description": "Throttle Plausibility"}]#1 is plausable, 0 implausable


TSVPackState = {0: "Boot", 1: "Charging", 2: "Charged", 3: "Low Current Output", 4: "Fault", 5: "Dead", 6: "Ready"}
TSIPackState = {0: "Idle", 1: "Setup Drive", 2: "Drive", 3: "Setup Idle", 4:"OverCurrent"}

displayDict = {"VS State": '-  ', "VS Session": '-', "VS Time": '-'}

#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
session = {"Session":0}

#Strings for error messages on GLV Display
errorDict = {"Error1": "LEV SCADA", "Error2": "-", "Error3": "-", "Error4": "-"}

# Dictionary for keeping track of the minimum cell voltage and maximum temp for each pack
packList =[{"pack": 1, "minCellVolt": 5, "maxCellTemp": 0},
		   {"pack": 2, "minCellVolt": 5, "maxCellTemp": 0},
		   {"pack": 3, "minCellVolt": 5, "maxCellTemp": 0},
	 	   {"pack": 4, "minCellVolt": 5, "maxCellTemp": 0}]

#Variables for storing
global record_button
global write_screen
global session_timestamp
global error_string
global critical_error
global min_volt_cell
global max_temp_cell
global throttle_plausibility
global airs_status
global brake_status
record_button = False
critical_error = False
write_screen = (False, 0)
session_timestamp = 0
min_volt_cell = 0
max_temp_cell = 0
throttle_plausibility = 0 #1 = Plausible: 0 is implausible
airs_status = 0
brake_status = 0

error_string = errorDict["Error1"] + '\n' + errorDict["Error2"] + '\n' + errorDict["Error3"] + '\n' + errorDict["Error4"]

def timer():
	"""Simple timer function that returns the number of seconds in now()

    Returns:
        int: number of seconds in datetime.now()

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
	now = datetime.now()
	nowSeconds = datetime.strftime(now, '%s')
	intSeconds = int(nowSeconds) % 60
	return intSeconds

def send_throttle_control(throttleControl):
	"""Function to send a signal to the TSI when we need to drop out drive mode

    Args:
        throttleControl (int): The value we are sending.

    Returns:
        int: The return value. True for success, False otherwise.

    """
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
	msg = can.Message(arbitration_id=0x010, data=[throttleControl], extended_id=False)
	bus.send(msg)

def twos_comp(val, bits):
    """compute the 2's complement of int value val

    Args:
        val (int): The value we are converting to 2's complement.
        bits (int): number of bits in the val (8 * numBytes)

    Returns:
        int: computes the 2's complement value

    """
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

def process_can_data(address, data, dataLength, error_list, config_list):
	"""compute the 2's complement of int value val

    Args:
        address (int): address of the CAN packet.
        data (int): data in the CAN packet
        dataLength (int): number of bytes of data
        error_list (errorList()): 
        config_list (configList()): 

    Returns:
        creates datapoints and updates values on the display

    """

    global airs_status
    global brake_status
    global throttle_plausibility
    
	for item in listOfViewableData:

		#if the data point's address equals the one of the message, make a new datapoint
		if hex(item['address']) == address:

			newDataPoint = Datapoint()
			newDataPoint.sensor_id = item['id']
			newDataPoint.byte_length = item['byteLength']
			newDataPoint.count = item['count']
			newDataPoint.scalar = item['scalar']
			newDataPoint.sensor_name = item['description']
			newDataPoint.system = item['system']
			newDataPoint.sampleTime = item['sampleTime']
			newDataPoint.pack = item['pack']
			offset = int(item['offset'])

			# Handle the byte length on data points
			if item['byteLength'] > 1:

				formattedData = data[offset]

				# for the length of byte, append to formatted data
				for i in range(int(item['byteLength'])):
					if i == (item['byteLength'] - 1):
						break
					else:
						# NUM * 2^8 --> SHIFT LEFT 8
						formattedData = ((formattedData * 2**8) + data[offset + (i + 1)])

				newDataPoint.data = formattedData
			else:
				newDataPoint.data = data[offset]

			# Based on the scalar, shift the decimal point as necessary
			newDataPoint.data = twos_comp(int(newDataPoint.data), int(newDataPoint.byte_length * 8)) / newDataPoint.scalar

			if "State" in newDataPoint.sensor_name:
				if "TSI" in newDataPoint.sensor_name:
					newDataPoint.data = TSIPackState[newDataPoint.data]
				else:
					newDataPoint.data = TSVPackState[newDataPoint.data]

			item["displayValue"] = newDataPoint.data

			# Log data based on the sample time of the object
			if newDataPoint.system == 'MC':
				if (newDataPoint.sampleTime * 4) <= newDataPoint.count and item['data'] != newDataPoint.data:					
					now = datetime.now().strftime('%H:%M:%S')
					log_data(newDataPoint, error_list, config_list)
					item['updated'] = now
					item['count'] = 0
					item['data'] = newDataPoint.data
				else:
					item['count'] = newDataPoint.count + 1
			else:
				if newDataPoint.sampleTime <= newDataPoint.count and item['data'] != newDataPoint.data:					
					now = datetime.now().strftime('%H:%M:%S')
					log_data(newDataPoint, error_list, config_list)
					item['updated'] = now
					item['count'] = 0
					item['data'] = newDataPoint.data
				else:
					item['count'] = newDataPoint.count + 1

			########## STATUS INDICATORS ###########
			if newDataPoint.sensor_name == "Throttle Plausibility":
				throttle_plausibility = int(newDataPoint.data)
			if newDataPoint.sensor_name == "AIRS Status":
				airs_status = int(newDataPoint.data)
			if newDataPoint.sensor_name == "Brake Press":
				brake_status = int(newDataPoint.data)

			print("SENSOR: " + str(newDataPoint.sensor_name) + " VALUE: " + str(newDataPoint.data) + " COUNT: " + str(item['count']))

			# update screens
			# update_display_dict(newDataPoint)
			# update_dashboard_dict(newDataPoint)
			update_scada_table()

def receive_can():
	"""retrieves packets from the CAN bus and passes them on to be processed
    """
	session["Session"] = models.get_session()
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

	#Initialize the error list to zero
	error_list = errorList()

	#Get sensor thresholds from config file
	config_list = configList()
	config_list.populate_thresh_list()

	for msg in bus:
		# Set the address, data, and data length for each message
		address = hex(msg.arbitration_id)
		data = msg.data
		dataLength = msg.dlc

		process_can_data(address, data, dataLength, error_list, config_list)

def log_data(datapoint, error_list, config):
	"""Puts datapoints into the db

    Args:
        datapoint (Datapoint): the data of one sensor
        error_list (errorList()): 
        config (configList()): 

    """
	global record_button
	global session_timestamp
	global error_string
	global critical_error

	data = datapoint.data
	sensor_name = datapoint.sensor_name
	pack = datapoint.pack
	system = datapoint.system
	sensor_id = int(datapoint.sensor_id)

	#Places Pack number in the name to increase log readability
	if pack>0:
		name = str(sensor_name) + " Pack: " + str(pack)
	else:
		name = sensor_name

	#Number of times SCADA must see a bad value before it drops out of drive mode
	max_num_errors = 4

	#Time
	#now = datetime.now().strftime('%H:%M:%S')
	if session_timestamp == 0:
		elapsed_time = '00:00'
	elif session_timestamp == 1:
		elapsed_time = '00:00'
	else:
		now = datetime.now()
		differenceDT = now - session_timestamp
		differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)
		datetimeDiff = datetime.strptime(str(differenceNUM), '(%M, %S)')
		elapsed_time = datetimeDiff.strftime('%M:%S')

	#Runs through config list
	for sensor_info in config.sensor_thresh_list:
		if sensor_info.sensor_id == sensor_id:
			#Check thresholds

			#If the thresholds are the same in the config file sensor will not be flagged
			if (sensor_info.lower_threshold == sensor_info.upper_threshold):
				flag = False

			#Sensor data is within allowable range
			elif data > sensor_info.lower_threshold and data < sensor_info.upper_threshold:
				flag = False

				#Sensor is in range so we can reset the error count
				error_list.reset_num_errors(sensor_id)
			
			#Sensor data is not within allowable range. Flag and check if drop out of drive mode needed
			else:
				flag = True
				
				#Do not need to drop out
				if sensor_info.drop_out == 0:
					logging.warning('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s', session["Session"], elapsed_time, name, data)
					error1 = str(name) + ' has exceeded threshold. Value: ' + str(data)
					update_error_dict(error1)
				
				#Need to drop out
				elif sensor_info.drop_out == 1:
					#Need to see value over threshold four times before dropping out
					if error_list.get_num_errors(sensor_id) >= max_num_errors:
						print("CONFIRM CRITICAL ERROR")
						logging.critical('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s. Droppping out of Drive Mode', session["Session"], elapsed_time, name, data)

						#Drop out call
						send_throttle_control(1)
						error1 = str(name) + ' has exceeded threshold. Value: ' + str(data)
						update_error_dict(error1)
						error2 = 'Drop out of Drive Mode'
						update_error_dict(error2)

						#Now that the error has been seen enough times it is set to critical.
						error_list.set_critical_error(sensor_id)

					#Error has been seen a few times already but it is not necesarily a critical error
					else:
						logging.critical('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s', session["Session"], elapsed_time, name, data)
						error1 = str(name) + ' has exceeded threshold. Value: ' + str(data)
						update_error_dict(error1)

			#Check every error in list to see if any of them are critical
			critical_error = error_list.check_critical_errors()

			#Store in database if record button is true
			if (record_button is True and sensor_info.log_en == 1):
				print("Logged")
				models.Data.create(sensor_id=sensor_id,sensorName=sensor_name, data=data, time=elapsed_time, system=system, pack=pack, flagged=flag, session_id=session["Session"], csv_out=sensor_info.csv_en)

def fix_decimal_places(decimalValue, desiredDecimalPlaces):
	"""Fix the number of decimal places to what you want

    Args:
        decimalValue (float): value we want change the number of decimal places
        desiredDecimalPlaces (int): number of decimal places we want

    Returns:
        str: value with the desired number of decimal places

    """
	# Data as a String
	dataString = str(decimalValue)

	if dataString == '-':
		return dataString
	elif desiredDecimalPlaces == 0:
		return str(int(decimalValue))
	else:
		# Make sure the new data has three decimal places
		decimalPlaces = Decimal(dataString).as_tuple().exponent * -1

		# Append or removed from the data string until we have the correct number of decimal places
		while decimalPlaces != desiredDecimalPlaces:

			if decimalPlaces > desiredDecimalPlaces:
				dataString = dataString[:-1]
				decimalPlaces = Decimal(dataString).as_tuple().exponent * -1

			elif decimalPlaces < desiredDecimalPlaces:
				if decimalPlaces == 0:
					dataString = dataString + ".0"
				else:
					dataString = dataString + "0"
				decimalPlaces = Decimal(dataString).as_tuple().exponent * -1

		return dataString

def update_scada_table():
	"""Updates the VSCADA table on the display indepent of CAN data

    """
	global record_button
	global session_timestamp

	########## VSCADA TABLE ##########
	displayDict["VS Session"] = session["Session"]

	# check if we are recording
	if record_button == True:
		displayDict["VS State"] = "REC"
	else:
		displayDict["VS State"] = "Idle"

	# check the timestamp value
	if session_timestamp == 0:
		displayDict["VS Time"] = 0
	elif session_timestamp == 1:
		pass
	else:
		now = datetime.now()
		differenceDT = now - session_timestamp
		differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)
		datetimeDiff = datetime.strptime(str(differenceNUM), '(%M, %S)')
		displayDict["VS Time"] = datetimeDiff.strftime('%M:%S')

def make_message_twenty_chars(sensorName, data, recording):
	"""In order to write to the dashboard display, the message needs to be 20 chars, so this funct will handle that

    Args:
        sensorName (str): name of sensor
        data (str or float): value we want displayed
        recording (bool): boolean value based on whether or not we are currently recording

    Returns:
    	twentyChars (str): str that is twenty characters long to be displayed

    """
	twentyChars = "" + sensorName + ": " +str(data)
	while len(twentyChars) < 20:
		if recording == False:
			twentyChars = twentyChars + " "
		else:
			if len(twentyChars) > 16:
				twentyChars = twentyChars + "*"
			else:
				twentyChars = twentyChars + " "
	return twentyChars

def update_dashboard_recording():
	"""Updates the drivers display and adds stars to the dashboard if we are recording

    """
	global record_button
	# Get the RPM
	if listOfViewableData[105 - 1]['displayValue'] == '-':
		rpm = 0
		mph = '-'
	else:
		rpm = listOfViewableData[105 - 1]['displayValue']
		# Formula for calculating MPH from RPM
		mph = float(rpm * (21/12) * (60/5280))
	writeToScreen(0, make_message_twenty_chars("MPH", fix_decimal_places(mph, 1), record_button))
	writeToScreen(1, make_message_twenty_chars(("A: " + fix_decimal_places(listOfViewableData[121 - 1]['displayValue'], 1) + " B"), fix_decimal_places(listOfViewableData[3 - 1]['displayValue'], 1), record_button))
	writeToScreen(2, make_message_twenty_chars("Motor Temp", fix_decimal_places(listOfViewableData[106 - 1]['displayValue'], 0), record_button))
	writeToScreen(3, make_message_twenty_chars("SOC", fix_decimal_places(find_min_soc(), 0), record_button))

def update_error_dict(error):
	"""Updates error dictionary with most recent error message

    Args:
        error (str): new error message

    """
	global error_string
	errorDict["Error1"] = errorDict["Error2"]
	errorDict["Error2"] = errorDict["Error3"]
	errorDict["Error3"] = errorDict["Error4"]
	errorDict["Error4"] = error
	error_string = str(errorDict["Error1"]) + '\n' + str(errorDict["Error2"]) + '\n' + str(errorDict["Error3"]) + '\n' + str(errorDict["Error4"])
	print(error_string)

def check_display_values():
	"""Check the frequency with which things are being updated, and remove old data from the table

    """
	# Iterate through the viewable data
	for item in listOfViewableData:
		# check if has ever been updated before, if not, just set to '-'
		if item['updated'] == 0:
			pass
		else:
			# check the last time that dict was updated
			now = datetime.now()
			lastUpdated = datetime.strptime(str(item['updated']), '%H:%M:%S')

			# get the difference in times
			differenceDT = now - lastUpdated

			# get the difference in numbers rather than a datetime timedelta object
			differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)

			# check the difference vs the sample time
			if differenceNUM[1] > (3 * item['sampleTime']):
				item['displayValue'] = '-'

def export_data():
	"""Check if record button has been pressed. Export if stop button is pressed

    """
	#Exports data exactly one time after stop button is pressed
	models.export_csv(session["Session"])
	print("Exported Data {}".format(session["Session"]))

	#Increment session
	session["Session"] = session["Session"] + 1
	print("New session{}".format(session["Session"]))

# Comment this funct
def find_min_cell_volt(packNumber):
	listOfCellVoltages = []
	for item in listOfViewableData:
		if item['pack'] == packNumber and "Cell" in item['description'] and "Voltage" in item['description']:
			if item['displayValue'] == '-':
				pass
			elif item['displayValue'] > 4.5 or item['displayValue'] < 0.1:
				pass
			else:
				listOfCellVoltages.append(item['displayValue'])
	if listOfCellVoltages == []:
		return '-'
	else:
		return min(listOfCellVoltages)

#Comment this funct
def find_max_cell_temp(packNumber):
	listOfCellTemps = []
	for item in listOfViewableData:
		if item['pack'] == packNumber and "Cell" in item['description'] and "Temp" in item['description']:	
			if item['displayValue'] == '-':
				pass
			elif item['displayValue'] > 150 or item['displayValue'] < 0.1:
				pass
			else:
				listOfCellTemps.append(item['displayValue'])
	if listOfCellTemps == []:
		return '-'
	else:
		return max(listOfCellTemps)

#Comment this funct
def find_min_soc():
	listOfSOCs = []
	for item in listOfViewableData:
		if "SOC" in item['description']:
			if item['displayValue'] == '-':
				pass
			else:
				listOfSOCs.append(item['displayValue'])
	if listOfSOCs == []:
		return '-'
	else:
		return min(listOfSOCs)

# Thread to Monitor and Parse CAN bus Data
class CanMonitorThread(QtCore.QThread):

	def run(self):

		models.build_db()
		logging.basicConfig(filename='/home/pi/Desktop/VSCADA/log.log', level=logging.WARNING)

		while (True):
			# Receive can datapoint
			receive_can()


# Thread to Monitor and Parse CAN bus Data
class UIUpdateThread(QtCore.QThread):

	def run(self):

		models.build_db()
		logging.basicConfig(filename='/home/pi/Desktop/VSCADA/log.log', level=logging.WARNING)

		while (True):
			# Update UI
			update_scada_table()
			# check_display_dict()	


# Thread to update driver display and scan dashboard buttons
class ButtonMonitorThread(QtCore.QThread):

	def run(self):

		global record_button
		global write_screen
		global session_timestamp
		# Write initially to the screen
		writeToScreen(0, make_message_twenty_chars("MPH", '-', False))
		writeToScreen(1, make_message_twenty_chars(("A: - B"), '-', record_button))
		writeToScreen(2, make_message_twenty_chars("Motor Temp", '-', False))
		writeToScreen(3, make_message_twenty_chars("SOC", '-', False))
		while (True):

			######################## WRITE TO SCREEN ########################
			# Write to the dashboard
			update_dashboard_recording()

			######################## READ FROM BUTTONS ########################
			# Open Serial connection for reading
			ser = serial.Serial(portName, baudRate, timeout=2)

			# check if button was pressed
			readButtons = ser.read(10)

			#Starts recording
			if readButtons == check:
				print("Check")
				if record_button == False:
					record_button = True
					session_timestamp = datetime.now()
			#Stops recording and exports data
			elif readButtons == close:
				print("Close")
				if record_button == True:
					record_button = False
					session_timestamp = 1
					export_data()
			#Exports previous session data
			elif readButtons == right:
				print("Right")
				models.export_csv_previous(session["Session"])
			elif readButtons == left:
				send_throttle_control(1)
			#Close Connection
			ser.close()


class GuiUpdateThread(QtCore.QThread):
	'''
	GUI Update Thread

	This thread is responsible for updating the UI elements at a regular
	frequency determined by the global variable _pollFrequency. The system is
	updated every 1/_pollFrequency seconds.
	'''
	trigger = QtCore.pyqtSignal()
	def run(self):
		global _time

		while(True):
			self.msleep(1000 / _pollFrequency)

			_time += 1 / _pollFrequency

			# Update UI
			update_scada_table()

			self.trigger.emit()
			#self.emit(QtCore.SIGNAL('update()'))


class Window(QtWidgets.QWidget, ui.Ui_Form):
	global critical_error
	global throttle_plausibility
	global airs_status
	global brake_status
	#GUI Update Thread
	gui_update = None

	can_monitor = None
	# Define a new signal called 'trigger' that has no arguments.
	trigger = QtCore.pyqtSignal()

	def __init__(self):

		QtWidgets.QWidget.__init__(self)
		self.setupUi(self)

		#start gui as full screen
		#self.showFullScreen()
		self.showMaximized()

		#get update
		self.gui_update = GuiUpdateThread()
		self.can_monitor = CanMonitorThread()
		self.button_monitor = ButtonMonitorThread()
		self.ui_update = UIUpdateThread()

		#start updating
		self.gui_update.start()
		self.can_monitor.start()
		self.button_monitor.start()
		self.ui_update.start()

		# Connect the trigger signal to a slot under gui_update
		self.gui_update.trigger.connect(self.guiUpdate)

		# Emit the trigger signal (update once)
		self.gui_update.trigger.emit()

	def guiUpdate(self):
		global record_button
		global session_timestamp

		_translate = QtCore.QCoreApplication.translate

		#VSCADA
		self.VS_Session.display(str(displayDict["VS Session"]))
		self.VS_Time.display(str(displayDict["VS Time"]))
		self.VS_State.setText(str(displayDict["VS State"]))

		#Motor Controller
		self.Motor_RPM.display(fix_decimal_places(listOfViewableData[105 - 1]['displayValue'], 0))# Motor RPM
		self.Motor_Temp.display(fix_decimal_places(listOfViewableData[106 - 1]['displayValue'], 0))# Motor Temp
		self.Motor_Throttle.display(fix_decimal_places(listOfViewableData[113 - 1]['displayValue'], 2))# MC Throttle input

		#TSI
		self.TSI_IMD.display(fix_decimal_places(listOfViewableData[116 - 1]['displayValue'], 1))# TSI IMD
		self.TSI_Throttle_V.display(fix_decimal_places(listOfViewableData[117 - 1]['displayValue'], 2))# TSI Throttle Voltage
		self.TSI_Current.display(fix_decimal_places(listOfViewableData[121 - 1]['displayValue'], 1))# TSI Current

		#L table
		self.Voltage1.display(fix_decimal_places(listOfViewableData[2 - 1]['displayValue'], 1))#  Voltage P1
		self.Voltage2.display(fix_decimal_places(listOfViewableData[28 - 1]['displayValue'], 1))# Voltage P2
		self.Voltage3.display(fix_decimal_places(listOfViewableData[54 - 1]['displayValue'], 1))# Voltage P3
		self.Voltage4.display(fix_decimal_places(listOfViewableData[80 - 1]['displayValue'], 1))# Voltage P4
		self.Temp1.display(fix_decimal_places(find_max_cell_temp(1), 1))# Max Temp P1
		self.Temp2.display(fix_decimal_places(find_max_cell_temp(2), 1))# Max Temp P1
		self.Temp3.display(fix_decimal_places(find_max_cell_temp(3), 1))# Max Temp P1
		self.Temp4.display(fix_decimal_places(find_max_cell_temp(4), 1))# Max Temp P1
		self.SOC1.display(fix_decimal_places(listOfViewableData[4 - 1]['displayValue'], 0))#  SOC P1
		self.SOC2.display(fix_decimal_places(listOfViewableData[30 - 1]['displayValue'], 0))# SOC P2
		self.SOC3.display(fix_decimal_places(listOfViewableData[56 - 1]['displayValue'], 0))# SOC P3
		self.SOC4.display(fix_decimal_places(listOfViewableData[82 - 1]['displayValue'], 0))# SOC P4
		self.State1.setText(str(listOfViewableData[1 - 1]['displayValue']))#  State P1
		self.State2.setText(str(listOfViewableData[27 - 1]['displayValue']))# State P2
		self.State3.setText(str(listOfViewableData[53 - 1]['displayValue']))# State P3
		self.State4.setText(str(listOfViewableData[79 - 1]['displayValue']))# State P4
		self.MiniCellV1.display(fix_decimal_places(find_min_cell_volt(1), 3))# Min Cell Volt P1
		self.MiniCellV2.display(fix_decimal_places(find_min_cell_volt(2), 3))# Min Cell Volt P2
		self.MiniCellV3.display(fix_decimal_places(find_min_cell_volt(3), 3))# Min Cell Volt P3
		self.MiniCellV4.display(fix_decimal_places(find_min_cell_volt(4), 3))# Min Cell Volt P4
		#MC
		self.MC_Vol.display(fix_decimal_places(listOfViewableData[109 - 1]['displayValue'], 1))#   MC Voltage
		self.MC_Temp.display(fix_decimal_places(listOfViewableData[107 - 1]['displayValue'], 1))#  MC Temp
		self.MC_State.setText(fix_decimal_places(listOfViewableData[111 - 1]['displayValue'], 0))# MC State
		#TSI
		self.TSI_Vol.display(fix_decimal_places(listOfViewableData[120 - 1]['displayValue'], 1))# TS Voltage
		self.TSI_Temp.display(fix_decimal_places(listOfViewableData[122 - 1]['displayValue'], 1))# TS Temp
		self.TSI_State.setText(str(listOfViewableData[115 - 1]['displayValue']))
		#LOG
		self.Log.setPlainText(error_string)

		if critical_error:
			self.VS_State.setStyleSheet("background:red;color:white;")
		else:
			self.VS_State.setStyleSheet("background:white;color:black;")

		if throttle_plausibility is 1:
			self.TSI_Throttle_V.setStyleSheet("background:white;color:black;")
		else:
			self.TSI_Throttle_V.setStyleSheet("background:red;color:white;")

		if airs_status is 0:
			self.Airs.setStyleSheet("background: lightgreen; color: darkgreen")
		else:
			self.Airs.setStyleSheet("background: red; color: white")


		if brake_status is 0:
			self.Brake.setStyleSheet("background: lightgreen; color: darkgreen")
		else:
			self.Brake.setStyleSheet("background: red; color: white")

		if self.REC.isDown() is True:
			if record_button is False:
				self.REC.setStyleSheet("background: red; color: white")
				record_button = True
				session_timestamp = datetime.now()
			else:
				self.REC.setStyleSheet("background: rgb(139, 83, 93); color: white")
				record_button = False
				session_timestamp = 1
				export_data()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec())
