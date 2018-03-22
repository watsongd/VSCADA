import can
import time
import queue
import logging
import config
import models
import datetime
import collections

import sys
import random
import gui

import serial

from PyQt5 import QtCore, QtWidgets
from screenwrite import *

# initialization of serial port
portName = '/dev/ttyACM0'
baudRate = 115200

# byte arrays output of dashboard display key presses
up    = b'\x80\x01\x01q\xc2\x80\x01\x07G\xa7'
down  = b'\x80\x01\x02\xea\xf0\x80\x01\x08\xb0_'
left  = b'\x80\x01\x03c\xe1\x80\x01\t9N'
right = b'\x80\x01\x04\xdc\x95\x80\x01\n\xa2|'
check = b'\x80\x01\x05U\x84\x80\x01\x0b+m'
close = b'\x80\x01\x06\xce\xb6\x80\x01\x0c\x94\x19'

_pollFrequency = 3.0
#global time counter
_time = 0

# testNow = datetime.datetime.now().strftime('%H:%M:%S')

class Datapoint(object):

	def __init__(self):
		sensor_id = 0
		sensor_name = ""
		data = 0
		system = ""
		sampleTime = 15
		pack = None

class Error(object):

	def __init__(self, name, num_errors):
		self.name = name
		self.num_errors = num_errors


listOfViewableData = [{"address": 0x100, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":1, "description": "State"},
					  {"address": 0x100, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":2, "description": "Voltage"},
					  {"address": 0x100, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 1,  "updated": 0, "id":3, "description": "Current"},
					  {"address": 0x100, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":4, "description": "SOC"},
					  {"address": 0x101, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":5, "description": "Columbs"},
					  {"address": 0x101, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":6, "description": "Cell 1 Status"},
					  {"address": 0x101, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":7, "description": "Cell 2 Status"},
					  {"address": 0x101, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":8, "description": "Cell 3 Status"},
					  {"address": 0x101, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":9, "description": "Cell 4 Status"},
					  {"address": 0x102, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":10, "description": "Cell 5 Status"},
					  {"address": 0x102, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":11, "description": "Cell 6 Status"},
					  {"address": 0x102, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":12, "description": "Cell 7 Status"},

					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":13, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":14, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":15, "description": "Cell 2 Voltage"},
					  {"address": 0x103, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":16, "description": "Cell 3 Voltage"},
					  {"address": 0x103, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":17, "description": "Cell 4 Voltage"},
					  {"address": 0x103, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":18, "description": "Cell 5 Voltage"},
					  {"address": 0x103, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":19, "description": "Cell 6 Voltage"},
					  {"address": 0x104, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":20, "description": "Cell 7 Voltage"},

					  {"address": 0x104, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":21, "description": "Cell 1 Temp"},
					  {"address": 0x104, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":22, "description": "Cell 2 Temp"},
					  {"address": 0x104, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":23, "description": "Cell 3 Temp"},
					  {"address": 0x105, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":24, "description": "Cell 4 Temp"},
					  {"address": 0x105, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":25, "description": "Cell 5 Temp"},
					  {"address": 0x105, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 15, "updated": 0, "id":26, "description": "Cell 6 Temp"},
					  {"address": 0x105, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":27, "description": "Cell 7 Temp"},


					  {"address": 0x200, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":28, "description": "State"},
					  {"address": 0x200, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":29, "description": "Voltage"},
					  {"address": 0x200, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 1,  "updated": 0, "id":30, "description": "Current"},
					  {"address": 0x200, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":31, "description": "SOC"},
					  {"address": 0x201, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":32, "description": "Columbs"},

					  {"address": 0x201, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":33, "description": "Cell 1 Status"},
					  {"address": 0x201, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":34, "description": "Cell 2 Status"},
					  {"address": 0x201, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":35, "description": "Cell 3 Status"},
					  {"address": 0x201, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":36, "description": "Cell 4 Status"},
					  {"address": 0x202, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":37, "description": "Cell 5 Status"},
					  {"address": 0x202, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":38, "description": "Cell 6 Status"},
					  {"address": 0x202, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":39, "description": "Cell 7 Status"},

					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":40, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":41, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":42, "description": "Cell 2 Voltage"},
					  {"address": 0x203, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":43, "description": "Cell 3 Voltage"},
					  {"address": 0x203, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":44, "description": "Cell 4 Voltage"},
					  {"address": 0x203, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":45, "description": "Cell 5 Voltage"},
					  {"address": 0x203, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":46, "description": "Cell 6 Voltage"},
					  {"address": 0x204, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":47, "description": "Cell 7 Voltage"},

					  {"address": 0x204, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":48, "description": "Cell 1 Temp"},
					  {"address": 0x204, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":49, "description": "Cell 2 Temp"},
					  {"address": 0x204, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":50, "description": "Cell 3 Temp"},
					  {"address": 0x205, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":51, "description": "Cell 4 Temp"},
					  {"address": 0x205, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":52, "description": "Cell 5 Temp"},
					  {"address": 0x205, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":53, "description": "Cell 6 Temp"},
					  {"address": 0x205, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 15, "updated": 0, "id":54, "description": "Cell 7 Temp"},


					  {"address": 0x300, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":55, "description": "State"},
					  {"address": 0x300, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":56, "description": "Voltage"},
					  {"address": 0x300, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 1,  "updated": 0, "id":57, "description": "Current"},
					  {"address": 0x300, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":58, "description": "SOC"},
					  {"address": 0x301, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":59, "description": "Columbs"},

					  {"address": 0x301, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":60, "description": "Cell 1 Status"},
					  {"address": 0x301, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":62, "description": "Cell 2 Status"},
					  {"address": 0x301, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":63, "description": "Cell 3 Status"},
					  {"address": 0x301, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":64, "description": "Cell 4 Status"},
					  {"address": 0x302, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":65, "description": "Cell 5 Status"},
					  {"address": 0x302, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":66, "description": "Cell 6 Status"},
					  {"address": 0x302, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":67, "description": "Cell 7 Status"},

					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":68, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":69, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":70, "description": "Cell 2 Voltage"},
					  {"address": 0x303, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":71, "description": "Cell 3 Voltage"},
					  {"address": 0x303, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":72, "description": "Cell 4 Voltage"},
					  {"address": 0x303, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":73, "description": "Cell 5 Voltage"},
					  {"address": 0x303, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":74, "description": "Cell 6 Voltage"},
					  {"address": 0x304, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":75, "description": "Cell 7 Voltage"},

					  {"address": 0x304, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":76, "description": "Cell 1 Temp"},
					  {"address": 0x304, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":77, "description": "Cell 2 Temp"},
					  {"address": 0x304, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":78, "description": "Cell 3 Temp"},
					  {"address": 0x305, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":79, "description": "Cell 4 Temp"},
					  {"address": 0x305, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":80, "description": "Cell 5 Temp"},
					  {"address": 0x305, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":81, "description": "Cell 6 Temp"},
					  {"address": 0x305, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 15, "updated": 0, "id":82, "description": "Cell 7 Temp"},


					  {"address": 0x400, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":83, "description": "State"},
					  {"address": 0x400, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":84, "description": "Voltage"},
					  {"address": 0x400, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 1,  "updated": 0, "id":85, "description": "Current"},
					  {"address": 0x400, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":86, "description": "SOC"},
					  {"address": 0x401, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":87, "description": "Columbs"},

					  {"address": 0x401, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":88, "description": "Cell 1 Status"},
					  {"address": 0x401, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":89, "description": "Cell 2 Status"},
					  {"address": 0x401, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":90, "description": "Cell 3 Status"},
					  {"address": 0x401, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":91, "description": "Cell 4 Status"},
					  {"address": 0x402, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":92, "description": "Cell 5 Status"},
					  {"address": 0x402, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":93, "description": "Cell 6 Status"},
					  {"address": 0x402, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":94, "description": "Cell 7 Status"},

					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":95, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":96, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":97, "description": "Cell 2 Voltage"},
					  {"address": 0x403, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":98, "description": "Cell 3 Voltage"},
					  {"address": 0x403, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":99, "description": "Cell 4 Voltage"},
					  {"address": 0x403, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":100, "description": "Cell 5 Voltage"},
					  {"address": 0x403, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":101, "description": "Cell 6 Voltage"},
					  {"address": 0x404, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":102, "description": "Cell 7 Voltage"},

					  {"address": 0x404, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":103, "description": "Cell 1 Temp"},
					  {"address": 0x404, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":104, "description": "Cell 2 Temp"},
					  {"address": 0x404, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":105, "description": "Cell 3 Temp"},
					  {"address": 0x405, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":106, "description": "Cell 4 Temp"},
					  {"address": 0x405, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":107, "description": "Cell 5 Temp"},
					  {"address": 0x405, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":108, "description": "Cell 6 Temp"},
					  {"address": 0x405, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 15, "updated": 0, "id":109, "description": "Cell 7 Temp"},


					  {"address": 0x601, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 1,  "updated": 0, "id":110, "description": "Motor RPM"},
					  {"address": 0x601, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":111, "description": "Motor Temp"},
					  {"address": 0x601, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":112, "description": "Controller Temp"},
					  {"address": 0x601, "offset": 4, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 1,  "updated": 0, "id":113, "description": "RMS Current"},
					  {"address": 0x601, "offset": 6, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":114, "description": "Capacitor Voltage"},
					  {"address": 0x602, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":115, "description": "Stator Frequency"},
					  {"address": 0x602, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":116, "description": "Controller Fault Primary"},
					  {"address": 0x602, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":117, "description": "Controller Fault Secondary"},
					  {"address": 0x602, "offset": 4, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":118, "description": "Throttle Input"},
					  {"address": 0x602, "offset": 5, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 15, "updated": 0, "id":119, "description": "Brake Input"},


					  {"address": 0x0F2, "offset": 0, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":120, "description": "TSI State"},
					  {"address": 0x0F2, "offset": 1, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":121, "description": "IMD"},
					  {"address": 0x0F2, "offset": 3, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":122, "description": "Throttle Voltage"},
					  #{"address": 0x0F2, "offset": 4, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 15, "updated": 0, "id":1, "description": "Brake"},
					  {"address": 0x0F3, "offset": 0, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":123, "description": "TSV Voltage"},
					  {"address": 0x0F3, "offset": 2, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":124, "description": "TSV Current"},
					  {"address": 0x0F3, "offset": 4, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":125, "description": "TSI Temp"}]



TSVPackState = {0: "Boot", 1: "Charging", 2: "Charged", 3: "Low Current Output", 4: "Fault", 5: "Dead", 6: "Ready"}
TSIPackState = {0: "Idle", 1: "Setup Drive", 2: "Drive", 3: "Setup Idle", 4:"OverCurrent"}

displayDict = {"Voltage 1": '-', "Voltage 2": '-', "Voltage 3": '-', "Voltage 4": '-', "Current 1": '-', "Current 2": '-', "Current 3": '-', "Current 4": '-',
"TSI State": '-', "IMD": '-', "Brake": '-', "TSV Voltage": '-', "TSV Current": '-', "TSI Temp": '-', "Motor RPM": '-', "Motor Temp": '0'}

# dashboardDict = {"Motor RPM": "-", "TSV Current": "-", "Motor Temp": "-", "SOC": "-"}
dashboardDict = {"IMD": "-", "Throttle Voltage": "-", "TSV Voltage": "-", "TSI Temp": "-"}

#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
session = {"Session":0}

#Variables for storing
global record_button
global write_screen
record_button = False
write_screen = False

def timer():
   now = time.localtime(time.time())
   return now[5]

def send_throttle_control(throttleControl):
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
	msg = msg = can.Message(arbitration_id=0x010, data=[throttleControl], extended_id=False)
	bus.send(msg)

def parse():
	session["Session"] = models.get_session()
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
	error_list = []
	for msg in bus:
		# Set the address, data, and data length for each message
		address = hex(msg.arbitration_id)
		data = msg.data
		dataLength = msg.dlc

		# Iterate through the possible data points
		for item in listOfViewableData:

			#if the data point's address equals the one of the message, make a new datapoint
			if hex(item['address']) == address:

				newDataPoint = Datapoint()
				newDataPoint.sensor_id = item['id']
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

				# Based on the description, shift the decimal point as necessary
				if "Voltage" in newDataPoint.sensor_name:
					if "Cell" in newDataPoint.sensor_name:
						# mV --> V
						newDataPoint.data = newDataPoint.data / 1000
					else:
						newDataPoint.data = newDataPoint.data / 10

				if "Current" in newDataPoint.sensor_name:
					# mA --> A
					newDataPoint.data = newDataPoint.data / 1000

				if "Temp" in newDataPoint.sensor_name:
					if "Cell" in newDataPoint.sensor_name:
						newDataPoint.data = newDataPoint.data / 10

				if "State" in newDataPoint.sensor_name:
					if "TSI" in newDataPoint.sensor_name:
						newDataPoint.data = TSIPackState[newDataPoint.data]
					else:
						newDataPoint.data = TSVPackState[newDataPoint.data]


				# Log data based on the sample time of the object
				if timer() % item['sampleTime'] == 0:
					now = datetime.datetime.now().strftime('%H:%M:%S')
					if item['updated'] != now:
						log_data(newDataPoint, error_list)
						update_display_dict(newDataPoint)
						update_dashboard_dict(newDataPoint)
						item['updated'] = now
						print("LAST UPDATED: " + str(item['updated']))
						print(newDataPoint.sensor_name + ": " + str(newDataPoint.data))

				#Check if displays need to be updated with a '-'
				if timer() % 5 == 0:
					check_display_dict()


#Takes data from parse() and stores in db if recording.
def log_data(datapoint, error_list):

	global record_button

	data = datapoint.data
	sensor_name = datapoint.sensor_name
	pack = datapoint.pack
	system = datapoint.system
	sensor_id = datapoint.sensor_id

	#Time
	now = datetime.datetime.now().strftime('%H:%M:%S')

	for sensor_info in config.sensor_thresh_list:
		if sensor_info.name == sensor_name:
			#Check thresholds
			if (sensor_info.lower_threshold == sensor_info.upper_threshold):
				flag = False
			elif data > sensor_info.lower_threshold and data < sensor_info.upper_threshold:
				#Sensor data is within allowable range
				flag = False
			else:
				#Sensor data is not within allowable range. Flag and check if drop out of drive mode needed
				flag = True
				print (str(sensor_info.lower_threshold) + ',' + str(sensor_info.upper_threshold) + ',' + str(data))
				#Do not need to drop out
				if sensor_info.drop_out == 0:
					logging.warning('%s : %s has exceeded the given threshold. Value: %s', now, sensor_name, data)

				#Need to drop out
				if sensor_info.drop_out == 1:
					#DROP OUT CALL HERE
					logging.critical('%s : %s has exceeded the given threshold. Value: %s', now, sensor_name, data)

					if get_num_errors(error_list, sensor_name) >= 1:
						print("CONFIRM CRITICAL ERROR")
						#send_throttle_control(1)
			if record_button is True:
				print("Logged")
				models.Data.create(sensor_id=sensor_id,sensorName=sensor_name, data=data, time=now, system=system, pack=pack, flagged=flag, session_id=session["Session"])

# Updates the display dictionary that stores data that appears on the GLV screen
def update_display_dict(datapoint):
	if datapoint.pack > 0:
		name = datapoint.sensor_name + " " + str(datapoint.pack)
	else:
		name = datapoint.sensor_name
	if name in displayDict:
		displayDict[name] = datapoint.data


# In order to write to the dashboard display, the message needs to be 20 chars, so this funct will handle that
def makeMessageTwentyChars(sensorName, data):
	twentyChars = "" + sensorName + ": " +str(data)
	while len(twentyChars) < 20:
		twentyChars = twentyChars + " "
	return twentyChars

# Updates the dashboard dictionary that stores data that appears for the driver
def update_dashboard_dict(datapoint):
	global write_screen

	name = datapoint.sensor_name
	if name in dashboardDict:
		# for state of charge, we want to display the charge of the pack with the lowest value
		if "SOC" in name:
			currentLowest = displayDict["SOC"]
			if currentLowest == "-":
				curentLowest = 100
			if datapoint.data < currentLowest:
				displayDict["SOC"] = datapoint.data
			else:
				displayDict["SOC"] = currentLowest
		else:
			displayDict[name] = datapoint.data
			write_screen = True
			print("WRITE TO SCREEN IN UPDATE: " + str(write_screen) + "\n")

# Check the frequency with which things are being updated
def check_display_dict():
	for key in displayDict.keys():

		# find the corresponding dict to the display dict
		if "1" in key:
			pack = 1
			if "Voltage" in key:
				desc = "Voltage"
			elif "Current" in key:
				desc = "Current"
			else:
				desc = "SOMETHINGBROKE"
		elif "2" in key:
			pack = 2
			if "Voltage" in key:
				desc = "Voltage"
			elif "Current" in key:
				desc = "Current"
			else:
				desc = "SOMETHINGBROKE"
		elif "3" in key:
			pack = 3
			if "Voltage" in key:
				desc = "Voltage"
			elif "Current" in key:
				desc = "Current"
			else:
				desc = "SOMETHINGBROKE"
		elif "4" in key:
			pack = 4
			if "Voltage" in key:
				desc = "Voltage"
			elif "Current" in key:
				desc = "Current"
			else:
				desc = "SOMETHINGBROKE"
		else:
			pack = 0
			desc = key

		# Iterate through the viewable data
		for item in listOfViewableData:

			# Find the item with the matching description
			if item['pack'] == pack and item['description'] == desc:

				# check if has ever been updated before, if not, just set to '-'
				if item['updated'] == 0:
					displayDict[key] = '-'
				else:
					# check the last time that dict was updated
					now = datetime.datetime.now()
					lastUpdated = datetime.datetime.strptime(str(item['updated']), '%H:%M:%S')

					# get the difference in times
					differenceDT = now - lastUpdated
					#print ("Difference in times:" + str(differenceDT))

					# get the difference in numbers rather than a datetime timedelta object
					differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)
					#print ("Difference in numbers:" + str(differenceNUM))

					# check the difference vs the sample time
					if differenceNUM[1] > (3 * item['sampleTime']):
						displayDict[key] = '-'


#Check if record button has been pressed. Export if stop button is pressed
def export_data():
	#Exports data exactly one time after stop button is pressed
	models.export_csv(session["Session"])
	print("Exported Data {}".format(session["Session"]))
	session["Session"] = session["Session"] + 1
	print("New session{}".format(session["Session"]))

#Scans through err_list and returns number of times we've encountered the error
def get_num_errors(error_list, name):
	#Named tuple for tracking sensors that exceed thresholds

	#Possibly add an updated time to the tuple and compare to current time
	#If the time elapsed has exceeded 2 minutes, resets

	for error in error_list:
		if error.name == name:
			error.num_errors = error.num_errors + 1
			print (error.num_errors)
			return error.num_errors
	error = Error(name=name, num_errors=1)
	error_list.append(error)
	return 1

class CanMonitorThread(QtCore.QThread):

	def run(self):

		models.build_db()
		logging.basicConfig(filename='log.log', level=logging.WARNING)
		while (True):
			parse()

class ButtonMonitorThread(QtCore.QThread):

	def run(self):

		global record_button
		global write_screen
		while (True):

			# Open Serial connection
			ser = serial.Serial(portName, baudRate)

			# check if button was pressed
			readButtons = ser.read(10)
			if readButtons == check:
				print("Check")
				if record_button == False:
					record_button = True
			elif readButtons == close:
				print("Close")
				if record_button == True:
					record_button = False
					export_data()

			#Close Connection
			ser.close()

			print("WRITE TO SCREEN IN THREAD: " + str(write_screen) + "\n")

			# Write to the dashboard if a new value has been seen
			if write_screen:
				print("INSIDE IF STATEMENT\n")
				for key in dashboardDict.keys():
					if "IMD" in key:
						writeToScreen(0, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "Throttle Voltage" in key:
						writeToScreen(1, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "TSI Temp" in key:
						writeToScreen(2, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "TSV Voltage" in key:
						writeToScreen(3, makeMessageTwentyChars(key, dashboardDict[key]))
				write_screen = False

			if timer() % 5 == 0:
				check_display_dict()

class WriteToDashThread(QtCore.QThread):

	def run(self):

		while (True):

			# Every 2 seconds we update the Driver dash
			if timer() % 2 == 0:
				for key in dashboardDict.keys():
					if "IMD" in key:
						writeToScreen(0, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "Throttle Voltage" in key:
						writeToScreen(1, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "TSI Temp" in key:
						writeToScreen(2, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "TSV Voltage" in key:
						writeToScreen(3, makeMessageTwentyChars(key, dashboardDict[key]))


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


			self.trigger.emit()
			#self.emit(QtCore.SIGNAL('update()'))


class Window(QtWidgets.QWidget, gui.Ui_Form):

	#GUI Update Thread
	gui_update = None

	can_monitor = None
	# Define a new signal called 'trigger' that has no arguments.
	trigger = QtCore.pyqtSignal()

	def __init__(self):

		QtWidgets.QWidget.__init__(self)
		self.setupUi(self)

		#start gui as full screen
		self.showFullScreen()
		#self.getMaximized()

		#get update
		self.gui_update = GuiUpdateThread()
		self.can_monitor = CanMonitorThread()
		self.button_monitor = ButtonMonitorThread()
		# self.write_screen = WriteToDashThread()

		#start updating
		self.gui_update.start()
		self.can_monitor.start()
		self.button_monitor.start()
		# self.write_screen.start()

		# Connect the trigger signal to a slot under gui_update
		self.gui_update.trigger.connect(self.guiUpdate)

		# Emit the trigger signal (update once)
		self.gui_update.trigger.emit()

	def guiUpdate(self):
		_translate = QtCore.QCoreApplication.translate


		Vpack1 = str(displayDict["Voltage 1"]) + " V"
		Vpack2 = str(displayDict["Voltage 2"]) + " V"
		Vpack3 = str(displayDict["Voltage 3"]) + " V"
		Vpack4 = str(displayDict["Voltage 4"]) + " V"
		Ipack1 = str(displayDict["Current 1"]) + " A"
		Ipack2 = str(displayDict["Current 2"]) + " A"
		Ipack3  = str(displayDict["Current 3"]) + " A"
		Ipack4   = str(displayDict["Current 4"]) + " A"
		motorTemp = str(displayDict["Motor Temp"]) + " °C"
		motorRPM  = str(displayDict["Motor RPM"]) + " RPM"
		TSI_state = str(displayDict["TSI State"])
		TSI_imd   = str(displayDict["IMD"])
		TSI_temp  = str(displayDict["TSI Temp"])
		Vtsv	  = str(displayDict["TSV Voltage"]) + " V"
		Itsv     = str(displayDict["TSV Current"]) + " A"
		Sess    = str(session["Session"])

		#Set values for pack voltage and current
		item = self.Packs.item(0, 0)
		item.setText(_translate("Form", Vpack1))
		item = self.Packs.item(0, 1)
		item.setText(_translate("Form", Ipack1))
		item = self.Packs.item(1, 0)
		item.setText(_translate("Form", Vpack2))
		item = self.Packs.item(1, 1)
		item.setText(_translate("Form", Ipack2))
		item = self.Packs.item(2, 0)
		item.setText(_translate("Form", Vpack3))
		item = self.Packs.item(2, 1)
		item.setText(_translate("Form", Ipack3))
		item = self.Packs.item(3, 0)
		item.setText(_translate("Form", Vpack4))
		item = self.Packs.item(3, 1)
		item.setText(_translate("Form", Ipack4))
		item = self.Packs.item(4, 0)
		item.setText(_translate("Form", Vtsv))
		item = self.Packs.item(4, 1)
		item.setText(_translate("Form", Itsv))

		#Set values for motor items
		item = self.Motor.item(0, 0)
		item.setText(_translate("Form", motorTemp))
		item = self.Motor.item(1, 0)
		item.setText(_translate("Form", motorRPM))

		#Set values for TSI
		item = self.TSI.item(0, 0)
		item.setText(_translate("Form", TSI_state))
		item = self.TSI.item(0, 1)
		item.setText(_translate("Form", TSI_imd))
		item = self.TSI.item(0, 2)
		item.setText(_translate("Form", TSI_temp))

		item = self.tableWidget.item(0, 0)
		item.setText(_translate("Form", Sess))



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec())
