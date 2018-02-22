import sys
import random
import first


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


class Window(QtWidgets.QWidget, first.Ui_Form):

	#GUI Update Thread
	gui_update = None
	# Define a new signal called 'trigger' that has no arguments.
	trigger = QtCore.pyqtSignal()

	def __init__(self):

		QtWidgets.QWidget.__init__(self)
		self.setupUi(self)
		#connect Qt signals
		# ***************** Measurands Inputs ****************************
		#get update
		self.gui_update = GuiUpdateThread()

		#start updating
		self.gui_update.start()


		# Connect the trigger signal to a slot under gui_update
		self.gui_update.trigger.connect(self.guiUpdate)

		# Emit the trigger signal (update once)
		self.gui_update.trigger.emit()

	def guiUpdate(self):
		_translate = QtCore.QCoreApplication.translate


		Vpack1 = str(random.randint(1,101))
		Vpack2 = str(random.randint(1,101))
		Vpack3 = str(random.randint(1,101))
		Vpack4 = str(random.randint(1,101))
		Ipack1 = str(random.randint(1,101))
		Ipack2 = str(random.randint(1,101))
		Ipack3 = str(random.randint(1,101))
		Ipack4 = str(random.randint(1,101))
		motorTemp = str(random.randint(1,101))
		motorRPM  = str(random.randint(1,101))
		TSI_state = str(random.randint(1,101))
		TSI_imd   = str(random.randint(1,101))
		TSI_brake = str(random.randint(1,101))
		TSV_v	  = str(random.randint(1,101))
		TSV_i     = str(random.randint(1,101))
		TSV_temp  = str(random.randint(1,101))


		#Set values for pack voltage and current
		item = self.Packs.item(0, 0)
		item.setText(_translate("Form", Vpack1))
		item = self.Packs.item(0, 1)
		item.setText(_translate("Form", Vpack2))
		item = self.Packs.item(0, 2)
		item.setText(_translate("Form", Vpack3))
		item = self.Packs.item(0, 3)
		item.setText(_translate("Form", Vpack4))
		item = self.Packs.item(1, 0)
		item.setText(_translate("Form", Ipack1))
		item = self.Packs.item(1, 1)
		item.setText(_translate("Form", Ipack2))
		item = self.Packs.item(1, 2)
		item.setText(_translate("Form", Ipack3))
		item = self.Packs.item(1, 3)
		item.setText(_translate("Form", Ipack4))

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
		item.setText(_translate("Form", TSI_brake))

		#Set values for TSI
		item = self.TSV.item(0, 0)
		item.setText(_translate("Form", TSV_v))
		item = self.TSV.item(0, 1)
		item.setText(_translate("Form", TSV_i))
		item = self.TSV.item(0, 2)
		item.setText(_translate("Form", TSV_temp))




if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()

	sys.exit(app.exec())
