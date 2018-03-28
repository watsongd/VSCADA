import can
import time
import queue
import logging
import models
import datetime
import collections

import sys
import random
import ui

import serial

from PyQt5 import QtCore, QtWidgets
from screenwrite import *

from errorList import *
from config import *

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

listOfViewableData = [{"address": 0x100, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":1, "description": "State"},
					  {"address": 0x100, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":2, "description": "Voltage"},
					  {"address": 0x100, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 1,  "updated": 0, "id":3, "description": "Current"},
					  {"address": 0x100, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":4, "description": "SOC"},
					  {"address": 0x101, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":5, "description": "Columbs"},

					  {"address": 0x101, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":6, "description": "Cell 1 Status"},
					  {"address": 0x101, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":7, "description": "Cell 2 Status"},
					  {"address": 0x101, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":8, "description": "Cell 3 Status"},
					  {"address": 0x101, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":9, "description": "Cell 4 Status"},
					  {"address": 0x102, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":10, "description": "Cell 5 Status"},
					  {"address": 0x102, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":11, "description": "Cell 6 Status"},
					  {"address": 0x102, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":12, "description": "Cell 7 Status"},

					  {"address": 0x102, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":13, "description": "Cell 1 Voltage"},
					  {"address": 0x102, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":14, "description": "Cell 2 Voltage"},
					  {"address": 0x103, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":15, "description": "Cell 3 Voltage"},
					  {"address": 0x103, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":16, "description": "Cell 4 Voltage"},
					  {"address": 0x103, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":17, "description": "Cell 5 Voltage"},
					  {"address": 0x103, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":18, "description": "Cell 6 Voltage"},
					  {"address": 0x104, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":19, "description": "Cell 7 Voltage"},

					  {"address": 0x104, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":20, "description": "Cell 1 Temp"},
					  {"address": 0x104, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":21, "description": "Cell 2 Temp"},
					  {"address": 0x104, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":22, "description": "Cell 3 Temp"},
					  {"address": 0x105, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":23, "description": "Cell 4 Temp"},
					  {"address": 0x105, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":24, "description": "Cell 5 Temp"},
					  {"address": 0x105, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 1, "sampleTime": 5, "updated": 0, "id":25, "description": "Cell 6 Temp"},
					  {"address": 0x105, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":26, "description": "Cell 7 Temp"},


					  {"address": 0x200, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":27, "description": "State"},
					  {"address": 0x200, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":28, "description": "Voltage"},
					  {"address": 0x200, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 1,  "updated": 0, "id":29, "description": "Current"},
					  {"address": 0x200, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":30, "description": "SOC"},
					  {"address": 0x201, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":31, "description": "Columbs"},

					  {"address": 0x201, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":32, "description": "Cell 1 Status"},
					  {"address": 0x201, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":33, "description": "Cell 2 Status"},
					  {"address": 0x201, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":34, "description": "Cell 3 Status"},
					  {"address": 0x201, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":35, "description": "Cell 4 Status"},
					  {"address": 0x202, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":36, "description": "Cell 5 Status"},
					  {"address": 0x202, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":37, "description": "Cell 6 Status"},
					  {"address": 0x202, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":38, "description": "Cell 7 Status"},

					  {"address": 0x202, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":39, "description": "Cell 1 Voltage"},
					  {"address": 0x202, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":40, "description": "Cell 2 Voltage"},
					  {"address": 0x203, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":41, "description": "Cell 3 Voltage"},
					  {"address": 0x203, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":42, "description": "Cell 4 Voltage"},
					  {"address": 0x203, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":43, "description": "Cell 5 Voltage"},
					  {"address": 0x203, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":44, "description": "Cell 6 Voltage"},
					  {"address": 0x204, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":45, "description": "Cell 7 Voltage"},

					  {"address": 0x204, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":46, "description": "Cell 1 Temp"},
					  {"address": 0x204, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":47, "description": "Cell 2 Temp"},
					  {"address": 0x204, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":48, "description": "Cell 3 Temp"},
					  {"address": 0x205, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":49, "description": "Cell 4 Temp"},
					  {"address": 0x205, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":50, "description": "Cell 5 Temp"},
					  {"address": 0x205, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":51, "description": "Cell 6 Temp"},
					  {"address": 0x205, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 2, "sampleTime": 5, "updated": 0, "id":52, "description": "Cell 7 Temp"},


					  {"address": 0x300, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":53, "description": "State"},
					  {"address": 0x300, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":54, "description": "Voltage"},
					  {"address": 0x300, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 1,  "updated": 0, "id":55, "description": "Current"},
					  {"address": 0x300, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":56, "description": "SOC"},
					  {"address": 0x301, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":57, "description": "Columbs"},

					  {"address": 0x301, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":58, "description": "Cell 1 Status"},
					  {"address": 0x301, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":59, "description": "Cell 2 Status"},
					  {"address": 0x301, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":60, "description": "Cell 3 Status"},
					  {"address": 0x301, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":61, "description": "Cell 4 Status"},
					  {"address": 0x302, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":62, "description": "Cell 5 Status"},
					  {"address": 0x302, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":63, "description": "Cell 6 Status"},
					  {"address": 0x302, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":64, "description": "Cell 7 Status"},

					  {"address": 0x302, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":65, "description": "Cell 1 Voltage"},
					  {"address": 0x302, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":66, "description": "Cell 2 Voltage"},
					  {"address": 0x303, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":67, "description": "Cell 3 Voltage"},
					  {"address": 0x303, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":68, "description": "Cell 4 Voltage"},
					  {"address": 0x303, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":69, "description": "Cell 5 Voltage"},
					  {"address": 0x303, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":70, "description": "Cell 6 Voltage"},
					  {"address": 0x304, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":71, "description": "Cell 7 Voltage"},

					  {"address": 0x304, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":72, "description": "Cell 1 Temp"},
					  {"address": 0x304, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":73, "description": "Cell 2 Temp"},
					  {"address": 0x304, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":74, "description": "Cell 3 Temp"},
					  {"address": 0x305, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":75, "description": "Cell 4 Temp"},
					  {"address": 0x305, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":76, "description": "Cell 5 Temp"},
					  {"address": 0x305, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":77, "description": "Cell 6 Temp"},
					  {"address": 0x305, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 3, "sampleTime": 5, "updated": 0, "id":78, "description": "Cell 7 Temp"},


					  {"address": 0x400, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":79, "description": "State"},
					  {"address": 0x400, "offset": 1, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":80, "description": "Voltage"},
					  {"address": 0x400, "offset": 3, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 1,  "updated": 0, "id":81, "description": "Current"},
					  {"address": 0x400, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":82, "description": "SOC"},
					  {"address": 0x401, "offset": 0, "byteLength": 4, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":83, "description": "Columbs"},

					  {"address": 0x401, "offset": 4, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":84, "description": "Cell 1 Status"},
					  {"address": 0x401, "offset": 5, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":85, "description": "Cell 2 Status"},
					  {"address": 0x401, "offset": 6, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":86, "description": "Cell 3 Status"},
					  {"address": 0x401, "offset": 7, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":87, "description": "Cell 4 Status"},
					  {"address": 0x402, "offset": 0, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":88, "description": "Cell 5 Status"},
					  {"address": 0x402, "offset": 1, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":89, "description": "Cell 6 Status"},
					  {"address": 0x402, "offset": 2, "byteLength": 1, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":90, "description": "Cell 7 Status"},

					  {"address": 0x402, "offset": 5, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":91, "description": "Cell 1 Voltage"},
					  {"address": 0x402, "offset": 3, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":92, "description": "Cell 2 Voltage"},
					  {"address": 0x403, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":93, "description": "Cell 3 Voltage"},
					  {"address": 0x403, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":94, "description": "Cell 4 Voltage"},
					  {"address": 0x403, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":95, "description": "Cell 5 Voltage"},
					  {"address": 0x403, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":96, "description": "Cell 6 Voltage"},
					  {"address": 0x404, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":97, "description": "Cell 7 Voltage"},

					  {"address": 0x404, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":98, "description": "Cell 1 Temp"},
					  {"address": 0x404, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":99, "description": "Cell 2 Temp"},
					  {"address": 0x404, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":100, "description": "Cell 3 Temp"},
					  {"address": 0x405, "offset": 0, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":101, "description": "Cell 4 Temp"},
					  {"address": 0x405, "offset": 2, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":102, "description": "Cell 5 Temp"},
					  {"address": 0x405, "offset": 4, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":103, "description": "Cell 6 Temp"},
					  {"address": 0x405, "offset": 6, "byteLength": 2, "system": "TSV", "pack": 4, "sampleTime": 5, "updated": 0, "id":104, "description": "Cell 7 Temp"},


					  {"address": 0x601, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 1, "updated": 0, "id":105, "description": "Motor RPM"},
					  {"address": 0x601, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":106, "description": "Motor Temp"},
					  {"address": 0x601, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":107, "description": "Controller Temp"},
					  {"address": 0x601, "offset": 4, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 1, "updated": 0, "id":108, "description": "RMS Current"},
					  {"address": 0x601, "offset": 6, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":109, "description": "Capacitor Voltage"},
					  {"address": 0x602, "offset": 0, "byteLength": 2, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":110, "description": "Stator Frequency"},
					  {"address": 0x602, "offset": 2, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":111, "description": "Controller Fault Primary"},
					  {"address": 0x602, "offset": 3, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":112, "description": "Controller Fault Secondary"},
					  {"address": 0x602, "offset": 4, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":113, "description": "Throttle Input"},
					  {"address": 0x602, "offset": 5, "byteLength": 1, "system": "MC", "pack": 0, "sampleTime": 5, "updated": 0, "id":114, "description": "Brake Input"},


					  {"address": 0x0F2, "offset": 0, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":115, "description": "TSI State"},
					  {"address": 0x0F2, "offset": 1, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":116, "description": "IMD"}, #IMD needs multiplied by 10
					  {"address": 0x0F2, "offset": 3, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":117, "description": "Throttle Voltage"}, #Needs multiplied by 10
					  {"address": 0x0F3, "offset": 0, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":118, "description": "TSV Voltage"},
					  {"address": 0x0F3, "offset": 2, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 1, "updated": 0, "id":119, "description": "TSV Current"},
					  {"address": 0x0F3, "offset": 4, "byteLength": 2, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":120, "description": "TSI Temp"},
					  {"address": 0x0F3, "offset": 6, "byteLength": 1, "system": "TSI", "pack": 0, "sampleTime": 5, "updated": 0, "id":121, "description": "Throttle Plausibility"}]


TSVPackState = {0: "Boot", 1: "Charging", 2: "Charged", 3: "Low Current Output", 4: "Fault", 5: "Dead", 6: "Ready"}
TSIPackState = {0: "Idle", 1: "Setup Drive", 2: "Drive", 3: "Setup Idle", 4:"OverCurrent"}

displayDict = {"Voltage 1": '-', "Voltage 2": '-', "Voltage 3": '-', "Voltage 4": '-',
			   "Temp 1": '-', "Temp 2": '-', "Temp 3": '-', "Temp 4": '-',
			   "State 1": '-', "State 2": '-', "State 3": '-', "State 4": '-',
			   "SOC 1": '-', "SOC 2": '-', "SOC 3": '-', "SOC 4": '-',
			   "Min Cell Volt 1": '-', "Min Cell Volt 2": '-', "Min Cell Volt 3": '-', "Min Cell Volt 4": '-',
			   "MC Voltage": '-', "MC Temp": '-', "MC State": '-',
			   "TS Voltage": '-', "TS Temp": '-', "TS State": '-',
			   "Motor RPM": '-', "Motor Temp": '-', "MC Throt Input": '-',
			   "TSI IMD": '-', "TSI Current": '-', "TSI Throt Volt": '-',
			   "VS State": '-', "VS Session": '-', "VS Time": '-'}

dashboardDict = {"Motor RPM": "-", "TSV Current": "-", "Motor Temp": "-", "SOC": "-"}

#Session is just an int that keeps track of when recording starts. If recording stops, the current session is exported and the session increments
session = {"Session":0}

#Strings for error messages on GLV Display
errorDict = {"Error1": "LEV SCADA", "Error2": "-", "Error3": "-", "Error4": "-", "Error5": "-"}

#Variables for storing
global record_button
global write_screen
global session_timestamp
global error_string
record_button = False
write_screen = False
session_timestamp = 0
error_string = errorDict["Error1"] + '\n' + errorDict["Error2"] + '\n' + errorDict["Error3"] + '\n' + errorDict["Error4"] + '\n' + errorDict["Error5"]

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
	#Initialize the error list to zero
	error_list = errorList()

	#Get sensor thresholds from config file
	config = config()
	ccnfig.populate_thresh_list()

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
				if newDataPoint.pack > 0:
					if "Voltage" in newDataPoint.sensor_name:
						if "Cell" in newDataPoint.sensor_name:
							# mV --> V
							newDataPoint.data = newDataPoint.data / 1000
						else:
							newDataPoint.data = newDataPoint.data / 10

					elif "Current" in newDataPoint.sensor_name:
						# mA --> A
						newDataPoint.data = newDataPoint.data / 1000

					elif "Temp" in newDataPoint.sensor_name:
						if "Cell" in newDataPoint.sensor_name:
							newDataPoint.data = newDataPoint.data / 10

				if "State" in newDataPoint.sensor_name:
					if "TSI" in newDataPoint.sensor_name:
						newDataPoint.data = TSIPackState[newDataPoint.data]
					else:
						newDataPoint.data = TSVPackState[newDataPoint.data]

				if "Capacitor Voltage" in newDataPoint.sensor_name:
					newDataPoint.data = newDataPoint.data / 10

				if "IMD" in newDataPoint.sensor_name:
					newDataPoint.data = newDataPoint.data / 10

				if "Throttle Voltage" in newDataPoint.sensor_name:
					newDataPoint.data = newDataPoint.data / 10

				if "Throttle Input" in newDataPoint.sensor_name:
					newDataPoint.data = newDataPoint.data / 10

				# Log data based on the sample time of the object
				if timer() % item['sampleTime'] == 0:
					now = datetime.datetime.now().strftime('%H:%M:%S')
					if item['updated'] != now:
						log_data(newDataPoint, error_list, config)
						# Record the time the datapoint was updated
						item['updated'] = now

				# update screens
				update_display_dict(newDataPoint)
				update_dashboard_dict(newDataPoint)

				#Check if displays need to be updated with a '-'
				if timer() % 5 == 0:
					check_display_dict()


#Takes data from parse() and stores in db if recording.
def log_data(datapoint, error_list, config):

	global record_button
	global session_timestamp
	global error_string

	data = datapoint.data
	sensor_name = datapoint.sensor_name
	pack = datapoint.pack
	system = datapoint.system
	sensor_id = datapoint.sensor_id

	#Time
	#now = datetime.datetime.now().strftime('%H:%M:%S')
	if session_timestamp == 0:
		elapsed_time = '00:00'
	elif session_timestamp == 1:
		elapsed_time = '00:00'
	else:
		now = datetime.datetime.now()
		differenceDT = now - session_timestamp
		differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)
		datetimeDiff = datetime.datetime.strptime(str(differenceNUM), '(%M, %S)')
		elapsed_time = datetimeDiff.strftime('%M:%S')

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
					logging.warning('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s', session["Session"], elapsed_time, sensor_name, data)
					error1 = str(sensor_name) + ' has exceeded threshold. Value: ' + str(data)
					update_error_dict(error1)
				#Need to drop out
				elif sensor_info.drop_out == 1:
					#DROP OUT CALL HERE
					#Need to see value over threshold four times before dropping out
					if error_list.get_num_errors(sensor_name) >= 4:
						print("CONFIRM CRITICAL ERROR")
						logging.critical('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s. Droppping out of Drive Mode', session["Session"], elapsed_time, sensor_name, data)
						#Drop out call
						send_throttle_control(1)
						error_list.reset_num_errors(sensor_name)
						error1 = str(sensor_name) + ' has exceeded threshold. Value: ' + str(data)
						update_error_dict(error1)
						error2 = 'Drop out of Drive Mode'
						update_error_dict(error2)
					else:
						logging.critical('Session: %d Time: %s : %s has exceeded the given threshold. Value: %s', session["Session"], elapsed_time, sensor_name, data)
						error1 = str(sensor_name) + ' has exceeded threshold. Value: ' + str(data)
						update_error_dict(error1)

			#Store in database if record button is true
			if record_button is True:
				print("Logged")
				models.Data.create(sensor_id=sensor_id,sensorName=sensor_name, data=data, time=elapsed_time, system=system, pack=pack, flagged=flag, session_id=session["Session"])

# Updates the display dictionary that stores data that appears on the GLV screen
def update_display_dict(datapoint):
	global record_button
	global session_timestamp

	# Handle data from the packs
	if datapoint.pack > 0:

		if "Cell" in datapoint.sensor_name:
			if "Voltage" in datapoint.sensor_name:
				name = "Min Cell Volt " + str(datapoint.pack)
			elif "Temp" in datapoint.sensor_name:
				name = "Temp " + str(datapoint.pack)
			else:
				name = "DONT CARE"
		else:
			name = datapoint.sensor_name + " " + str(datapoint.pack)

	# Handle data from other subsystems
	else:

		########## TSI TABLE ###########
		if "IMD" in datapoint.sensor_name:
			name = "TSI " + datapoint.sensor_name
		elif "TSV" and "Current" in datapoint.sensor_name:
			name = "TSI Current"
		elif "Throttle Voltage" in datapoint.sensor_name:
			name = "TSI Throt Volt"

		########## MC TABLE ##########
		elif "Motor RPM" in datapoint.sensor_name:
			name = datapoint.sensor_name
		elif "Motor Temp" in datapoint.sensor_name:
			name = datapoint.sensor_name
		elif "Throttle Input" in datapoint.sensor_name:
			name = "MC Throt Input"

		########## "L" TABLE ##########
		elif "Capacitor Voltage" in datapoint.sensor_name:
			name = "MC Voltage"
		elif "Controller Temp" in datapoint.sensor_name:
			name = "MC Temp"
		elif "Controller Fault Primary" in datapoint.sensor_name:
			name = "MC State"
		elif "TSV Voltage" in datapoint.sensor_name:
			name = "TS Voltage"
		elif "TSI Temp" in datapoint.sensor_name:
			name = "TS Temp"
		elif "TSI State" in datapoint.sensor_name:
			name = "TS State"

		else:
			name = "NOT IN DISPLAY DICT"

	# If the name is in the display dictionary, update the value
	if name in displayDict:

		# If the name is max temp or min volt of cell, make comparisons
		if "Min Cell Volt" in name:
			lowestCellVolt = displayDict[name]

			# If its the first entry, directly input
			if lowestCellVolt == '-':
				displayDict[name] = datapoint.data

			# Otherwise, take the lowest
			elif lowestCellVolt > datapoint.data:
				displayDict[name] = datapoint.data

			else:
				displayDict[name] = displayDict[name]
		elif "Temp " in name:
			maxTemp = displayDict[name]

			# If its the first entry, directly input
			if maxTemp == '-':
				displayDict[name] = datapoint.data

			# Otherwise, take the highest
			elif maxTemp < datapoint.data:
				if datapoint.data > 150:
					pass
				else:
					displayDict[name] = datapoint.data
			else:
				displayDict[name] = displayDict[name]
		else:
			displayDict[name] = datapoint.data

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
		now = datetime.datetime.now()
		differenceDT = now - session_timestamp
		differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)
		datetimeDiff = datetime.datetime.strptime(str(differenceNUM), '(%M, %S)')
		displayDict["VS Time"] = datetimeDiff.strftime('%M:%S')

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
			currentLowest = dashboardDict["SOC"]
			if currentLowest == "-":
				dashboardDict["SOC"] = datapoint.data
			elif datapoint.data < currentLowest:
				dashboardDict["SOC"] = datapoint.data
			else:
				dashboardDict["SOC"] = currentLowest
		else:
			dashboardDict[name] = datapoint.data
			write_screen = True

# Updates error dictionary with most recent error message
def update_error_dict(error):
	global error_string
	errorDict["Error1"] = errorDict["Error2"]
	errorDict["Error2"] = errorDict["Error3"]
	errorDict["Error3"] = errorDict["Error4"]
	errorDict["Error4"] = errorDict["Error5"]
	errorDict["Error5"] = error
	error_string = str(errorDict["Error1"]) + '\n' + str(errorDict["Error2"]) + '\n' + str(errorDict["Error3"]) + '\n' + str(errorDict["Error4"]) + '\n' + str(errorDict["Error5"])
	print(error_string)

# Check the frequency with which things are being updated
def check_display_dict():
	for key in displayDict.keys():

		#get the last character in the key
		lastChar = key[-1:]

		# check if the last character in the key is a number or not
		if lastChar.isalpha() == False:
			pack = int(lastChar)
			if "Voltage" in key:
				desc = "Voltage"
			elif "Temp" in key:
				desc = "Temp"
			elif "State" in key:
				desc = "State"
			elif "SOC" in key:
				desc = "Temp"
			elif "Min Cell Volt" in key:
				desc = "Min Cell Volt"
		else:
			pack = 0
			if "MC Voltage" in key:
				desc = "Capacitor Voltage"
			elif "MC Temp" in key:
				desc = "Controller Temp"
			elif "MC Throt Input" in key:
				desc = "Throttle Input"
			elif "IMD" in key:
				desc = "IMD"
			elif "TSI Throt Volt" in key:
				desc = "Throttle Voltage"
			else:
				desc = key

		# Values for keeping track of the last time the Min Cell Voltage and Max Cell Temp were updated
		oldestUpdateMCV = 0
		oldestUpdateMCT = 0

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

					# get the difference in numbers rather than a datetime timedelta object
					differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)

					# check the difference vs the sample time
					if differenceNUM[1] > (3 * item['sampleTime']):
						displayDict[key] = '-'

			# For the ones without a matching description, we need to check every cell for the oldest update time
			else:
				if "Min Cell Volt" in desc:

					# Look through every cell in the pack to find the most recent update time
					for i in range(7):
						if item['pack'] == pack and item['description'] == "Cell " + str(i + 1) + " Voltage":
							# check if has ever been updated before, if not, just set to '-'
							if item['updated'] == 0 and oldestUpdateMCV == 0:
								pass
							else:
								cellUpdated= datetime.datetime.strptime(str(item['updated']), '%H:%M:%S')

								if oldestUpdateMCV == 0:
									oldestUpdateMCV = cellUpdated
								elif oldestUpdateMCV > cellUpdated:
									oldestUpdateMCV = cellUpdated

					if oldestUpdateMCV != 0:

						# check the last time that dict was updated
						now = datetime.datetime.now()

						# get the difference in times
						differenceDT = now - oldestUpdateMCV

						# get the difference in numbers rather than a datetime timedelta object
						differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)

						# check the difference vs the sample time
						if differenceNUM[1] > (3 * item['sampleTime']):
							displayDict[key] = '-'

				elif "Temp" in desc:

					# Look through every cell in the pack to find the most recent update time
					for i in range(7):
						if item['pack'] == pack and item['description'] == "Cell " + str(i + 1) + " Temp":
							# check if has ever been updated before, if not, just set to '-'
							if item['updated'] == 0 and oldestUpdateMCT == 0:
								pass
							else:
								cellUpdated= datetime.datetime.strptime(str(item['updated']), '%H:%M:%S')

								if oldestUpdateMCT == 0:
									oldestUpdateMCT = cellUpdated
								elif oldestUpdateMCT > cellUpdated:
									oldestUpdateMCT = cellUpdated

					if oldestUpdateMCT != 0:

						# check the last time that dict was updated
						now = datetime.datetime.now()

						# get the difference in times
						differenceDT = now - oldestUpdateMCT

						# get the difference in numbers rather than a datetime timedelta object
						differenceNUM = divmod(differenceDT.days * 86400 + differenceDT.seconds, 60)

						# check the difference vs the sample time
						if differenceNUM[1] > (3 * item['sampleTime']):
							displayDict[key] = '-'


#Check if record button has been pressed. Export if stop button is pressed
def export_data():
	#Exports data exactly one time after stop button is pressed
	models.export_csv(session["Session"])
	print("Exported Data {}".format(session["Session"]))

	#Increment session
	session["Session"] = session["Session"] + 1
	print("New session{}".format(session["Session"]))

#Thread to Monitor and Parse CAN bus Data
class CanMonitorThread(QtCore.QThread):

	def run(self):

		models.build_db()
		logging.basicConfig(filename='/home/pi/Desktop/VSCADA/log.log', level=logging.WARNING)
		while (True):
			parse()

#Thread to update driver display and scan dashboard buttons
class ButtonMonitorThread(QtCore.QThread):

	def run(self):

		global record_button
		global write_screen
		global session_timestamp

		while (True):

			######################## WRITE TO SCREEN ########################
			# Write to the dashboard if a new value has been seen
			if write_screen:
				for key in dashboardDict.keys():
					if "Motor RPM" in key:
						writeToScreen(0, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "Current" in key:
						writeToScreen(1, makeMessageTwentyChars("Current", dashboardDict[key]))
					elif "Motor Temp" in key:
						writeToScreen(2, makeMessageTwentyChars(key, dashboardDict[key]))
					elif "SOC" in key:
						writeToScreen(3, makeMessageTwentyChars(key, dashboardDict[key]))
				write_screen = False

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
					session_timestamp = datetime.datetime.now()
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
			#Close Connection
			ser.close()

			if timer() % 5 == 0:
				check_display_dict()


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



class Window(QtWidgets.QWidget, ui.Ui_Form):

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

		#start updating
		self.gui_update.start()
		self.can_monitor.start()
		self.button_monitor.start()

		# Connect the trigger signal to a slot under gui_update
		self.gui_update.trigger.connect(self.guiUpdate)

		# Emit the trigger signal (update once)
		self.gui_update.trigger.emit()

	def guiUpdate(self):
		_translate = QtCore.QCoreApplication.translate


		#VSCADA
		self.VS_Session.display(str(displayDict["VS Session"]))
		self.VS_Time.display(str(displayDict["VS Time"]))
		self.VS_State.setText(str(displayDict["VS State"]))

		#Motor Controller
		self.Motor_RPM.display(str(displayDict["Motor RPM"]))
		self.Motor_Temp.display(str(displayDict["Motor Temp"]))
		self.Motor_Throttle.display(str(displayDict["MC Throt Input"]))

		#TSI
		self.TSI_IMD.display(str(displayDict["TSI IMD"]))
		self.TSI_Throttle_V.display(str(displayDict["TSI Throt Volt"]))
		self.TSI_Current.display(str(displayDict["TSI Current"]))

		#L table
		self.Voltage1.display(str(displayDict["Voltage 1"]))
		self.Voltage2.display(str(displayDict["Voltage 2"]))
		self.Voltage3.display(str(displayDict["Voltage 3"]))
		self.Voltage4.display(str(displayDict["Voltage 4"]))
		self.Temp1.display(str(displayDict["Temp 1"]))#°C
		self.Temp2.display(str(displayDict["Temp 2"]))#°C
		self.Temp3.display(str(displayDict["Temp 3"]))#°C
		self.Temp4.display(str(displayDict["Temp 4"]))#°C
		self.SOC1.display(str(displayDict["SOC 1"]))
		self.SOC2.display(str(displayDict["SOC 2"]))
		self.SOC3.display(str(displayDict["SOC 3"]))
		self.SOC4.display(str(displayDict["SOC 4"]))
		self.State1.setText(str(displayDict["State 1"]))
		self.State2.setText(str(displayDict["State 2"]))
		self.State3.setText(str(displayDict["State 3"]))
		self.State4.setText(str(displayDict["State 4"]))
		self.MiniCellV1.display(str(displayDict["Min Cell Volt 1"]))
		self.MiniCellV2.display(str(displayDict["Min Cell Volt 2"]))
		self.MiniCellV3.display(str(displayDict["Min Cell Volt 3"]))
		self.MiniCellV4.display(str(displayDict["Min Cell Volt 4"]))
		#MC
		self.MC_Vol.display(str(displayDict["MC Voltage"]))
		self.MC_Temp.display(str(displayDict["MC Temp"]))
		self.MC_State.setText(str(displayDict["MC State"]))
		#TSI
		self.TSI_Vol.display(str(displayDict["TS Voltage"]))
		self.TSI_Temp.display(str(displayDict["TS Temp"]))
		self.TSI_State.setText(str(displayDict["TS State"]))
		#LOG
		self.Log.setPlainText(error_string)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec())
