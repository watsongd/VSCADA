'''
install SIP Library
pip3 install SIP
install pyqt5 Library
pip3 install pyqt5
'''
import time


import sys
import random
import ui


from PyQt5 import QtCore, QtWidgets

_pollFrequency = 3.0
#global time counter
_time = 0





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

		#start updating
		self.gui_update.start()

		# Connect the trigger signal to a slot under gui_update
		self.gui_update.trigger.connect(self.guiUpdate)

		# Emit the trigger signal (update once)
		self.gui_update.trigger.emit()

	def guiUpdate(self):
		global record_button
		global session_timestamp

		_translate = QtCore.QCoreApplication.translate

		#VSCADA
		self.VS_Session.display("0")
		self.VS_Time.display("0")
		self.VS_State.setText("IDLE")

		#Motor Controller
		self.Motor_RPM.display("0")
		self.Motor_Temp.display("0")
		self.Motor_Throttle.display("0")

		#TSI
		self.TSI_IMD.display("0")
		self.TSI_Throttle_V.display("0")
		self.TSI_Current.display("0")

		#L table
		self.Voltage1.display("0")
		self.Voltage2.display("0")
		self.Voltage3.display("0")
		self.Voltage4.display("0")
		self.Temp1.display('0')#°C
		self.Temp2.display("0")#°C
		self.Temp3.display("0")#°C
		self.Temp4.display("0")#°C
		self.SOC1.display("0")
		self.SOC2.display("0")
		self.SOC3.display("0")
		self.SOC4.display("0")
		self.State1.setText("IDLE")
		self.State2.setText("IDLE")
		self.State3.setText("IDLE")
		self.State4.setText("IDLE")
		self.MiniCellV1.display("0")
		self.MiniCellV2.display("0")
		self.MiniCellV3.display("0")
		self.MiniCellV4.display("0")
		#MC
		self.MC_Vol.display("0")
		self.MC_Temp.display("0")
		self.MC_State.setText("IDLE")
		#TSI
		self.TSI_Vol.display("0")
		self.TSI_Temp.display("0")
		self.TSI_State.setText("IDLE")
		#LOG
		self.Log.setPlainText("LEFV VSCADA")



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec())
