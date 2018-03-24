# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(679, 446)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.Motor_RPM = QtWidgets.QLCDNumber(Form)
        self.Motor_RPM.setObjectName("Motor_RPM")
        self.gridLayout.addWidget(self.Motor_RPM, 1, 4, 1, 1)
        self.ThrottleIn = QtWidgets.QLabel(Form)
        self.ThrottleIn.setObjectName("ThrottleIn")
        self.gridLayout.addWidget(self.ThrottleIn, 3, 3, 1, 1)
        self.TSICurrent = QtWidgets.QLabel(Form)
        self.TSICurrent.setObjectName("TSICurrent")
        self.gridLayout.addWidget(self.TSICurrent, 3, 6, 1, 1)
        self.Voltage2 = QtWidgets.QLCDNumber(Form)
        self.Voltage2.setObjectName("Voltage2")
        self.gridLayout.addWidget(self.Voltage2, 8, 1, 1, 1)
        self.SOC1 = QtWidgets.QLCDNumber(Form)
        self.SOC1.setObjectName("SOC1")
        self.gridLayout.addWidget(self.SOC1, 7, 6, 1, 1)
        self.Motor_Throttle = QtWidgets.QLCDNumber(Form)
        self.Motor_Throttle.setObjectName("Motor_Throttle")
        self.gridLayout.addWidget(self.Motor_Throttle, 3, 4, 1, 1)
        self.SOC2 = QtWidgets.QLCDNumber(Form)
        self.SOC2.setObjectName("SOC2")
        self.gridLayout.addWidget(self.SOC2, 8, 6, 1, 1)
        self.State2 = QtWidgets.QLCDNumber(Form)
        self.State2.setObjectName("State2")
        self.gridLayout.addWidget(self.State2, 8, 4, 1, 1)
        self.VSCADA = QtWidgets.QLabel(Form)
        self.VSCADA.setAlignment(QtCore.Qt.AlignCenter)
        self.VSCADA.setObjectName("VSCADA")
        self.gridLayout.addWidget(self.VSCADA, 0, 0, 1, 2)
        self.Pack2 = QtWidgets.QLabel(Form)
        self.Pack2.setObjectName("Pack2")
        self.gridLayout.addWidget(self.Pack2, 8, 0, 1, 1)
        self.Motor_Temp = QtWidgets.QLCDNumber(Form)
        self.Motor_Temp.setObjectName("Motor_Temp")
        self.gridLayout.addWidget(self.Motor_Temp, 2, 4, 1, 1)
        self.VS_Session = QtWidgets.QLCDNumber(Form)
        self.VS_Session.setObjectName("VS_Session")
        self.gridLayout.addWidget(self.VS_Session, 2, 1, 1, 1)
        self.TSI_IMD = QtWidgets.QLCDNumber(Form)
        self.TSI_IMD.setObjectName("TSI_IMD")
        self.gridLayout.addWidget(self.TSI_IMD, 1, 7, 1, 1)
        self.MotorTemp = QtWidgets.QLabel(Form)
        self.MotorTemp.setObjectName("MotorTemp")
        self.gridLayout.addWidget(self.MotorTemp, 2, 3, 1, 1)
        self.ThrottleV = QtWidgets.QLabel(Form)
        self.ThrottleV.setObjectName("ThrottleV")
        self.gridLayout.addWidget(self.ThrottleV, 2, 6, 1, 1)
        self.MotorRPM = QtWidgets.QLabel(Form)
        self.MotorRPM.setObjectName("MotorRPM")
        self.gridLayout.addWidget(self.MotorRPM, 1, 3, 1, 1)
        self.TSI_Throttle_V = QtWidgets.QLCDNumber(Form)
        self.TSI_Throttle_V.setObjectName("TSI_Throttle_V")
        self.gridLayout.addWidget(self.TSI_Throttle_V, 2, 7, 1, 1)
        self.Temp2 = QtWidgets.QLCDNumber(Form)
        self.Temp2.setObjectName("Temp2")
        self.gridLayout.addWidget(self.Temp2, 8, 3, 1, 1)
        self.TSIIMD = QtWidgets.QLabel(Form)
        self.TSIIMD.setObjectName("TSIIMD")
        self.gridLayout.addWidget(self.TSIIMD, 1, 6, 1, 1)
        self.TSI_Current = QtWidgets.QLCDNumber(Form)
        self.TSI_Current.setObjectName("TSI_Current")
        self.gridLayout.addWidget(self.TSI_Current, 3, 7, 1, 1)
        self.Voltage = QtWidgets.QLabel(Form)
        self.Voltage.setObjectName("Voltage")
        self.gridLayout.addWidget(self.Voltage, 6, 1, 1, 1)
        self.Temp = QtWidgets.QLabel(Form)
        self.Temp.setObjectName("Temp")
        self.gridLayout.addWidget(self.Temp, 6, 3, 1, 1)
        self.State = QtWidgets.QLabel(Form)
        self.State.setObjectName("State")
        self.gridLayout.addWidget(self.State, 6, 4, 1, 1)
        self.SOC = QtWidgets.QLabel(Form)
        self.SOC.setObjectName("SOC")
        self.gridLayout.addWidget(self.SOC, 6, 6, 1, 1)
        self.Mini_Cell_Voltage = QtWidgets.QLabel(Form)
        self.Mini_Cell_Voltage.setObjectName("Mini_Cell_Voltage")
        self.gridLayout.addWidget(self.Mini_Cell_Voltage, 6, 7, 1, 1)
        self.Pack1 = QtWidgets.QLabel(Form)
        self.Pack1.setObjectName("Pack1")
        self.gridLayout.addWidget(self.Pack1, 7, 0, 1, 1)
        self.Voltage1 = QtWidgets.QLCDNumber(Form)
        self.Voltage1.setObjectName("Voltage1")
        self.gridLayout.addWidget(self.Voltage1, 7, 1, 1, 1)
        self.Temp1 = QtWidgets.QLCDNumber(Form)
        self.Temp1.setObjectName("Temp1")
        self.gridLayout.addWidget(self.Temp1, 7, 3, 1, 1)
        self.State1 = QtWidgets.QLCDNumber(Form)
        self.State1.setObjectName("State1")
        self.gridLayout.addWidget(self.State1, 7, 4, 1, 1)
        self.MiniCellV1 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV1.setObjectName("MiniCellV1")
        self.gridLayout.addWidget(self.MiniCellV1, 7, 7, 1, 1)
        self.VStime = QtWidgets.QLabel(Form)
        self.VStime.setObjectName("VStime")
        self.gridLayout.addWidget(self.VStime, 3, 0, 1, 1)
        self.MiniCellV2 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV2.setObjectName("MiniCellV2")
        self.gridLayout.addWidget(self.MiniCellV2, 8, 7, 1, 1)
        self.Pack3 = QtWidgets.QLabel(Form)
        self.Pack3.setObjectName("Pack3")
        self.gridLayout.addWidget(self.Pack3, 9, 0, 1, 1)
        self.Voltage3 = QtWidgets.QLCDNumber(Form)
        self.Voltage3.setObjectName("Voltage3")
        self.gridLayout.addWidget(self.Voltage3, 9, 1, 1, 1)
        self.Temp3 = QtWidgets.QLCDNumber(Form)
        self.Temp3.setObjectName("Temp3")
        self.gridLayout.addWidget(self.Temp3, 9, 3, 1, 1)
        self.State3 = QtWidgets.QLCDNumber(Form)
        self.State3.setObjectName("State3")
        self.gridLayout.addWidget(self.State3, 9, 4, 1, 1)
        self.SOC3 = QtWidgets.QLCDNumber(Form)
        self.SOC3.setObjectName("SOC3")
        self.gridLayout.addWidget(self.SOC3, 9, 6, 1, 1)
        self.MiniCellV3 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV3.setObjectName("MiniCellV3")
        self.gridLayout.addWidget(self.MiniCellV3, 9, 7, 1, 1)
        self.Pack4 = QtWidgets.QLabel(Form)
        self.Pack4.setObjectName("Pack4")
        self.gridLayout.addWidget(self.Pack4, 10, 0, 1, 1)
        self.Voltage4 = QtWidgets.QLCDNumber(Form)
        self.Voltage4.setObjectName("Voltage4")
        self.gridLayout.addWidget(self.Voltage4, 10, 1, 1, 1)
        self.Temp4 = QtWidgets.QLCDNumber(Form)
        self.Temp4.setObjectName("Temp4")
        self.gridLayout.addWidget(self.Temp4, 10, 3, 1, 1)
        self.State4 = QtWidgets.QLCDNumber(Form)
        self.State4.setObjectName("State4")
        self.gridLayout.addWidget(self.State4, 10, 4, 1, 1)
        self.SOC4 = QtWidgets.QLCDNumber(Form)
        self.SOC4.setObjectName("SOC4")
        self.gridLayout.addWidget(self.SOC4, 10, 6, 1, 1)
        self.MiniCellV4 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV4.setObjectName("MiniCellV4")
        self.gridLayout.addWidget(self.MiniCellV4, 10, 7, 1, 1)
        self.MC = QtWidgets.QLabel(Form)
        self.MC.setObjectName("MC")
        self.gridLayout.addWidget(self.MC, 11, 0, 1, 1)
        self.MC_Vol = QtWidgets.QLCDNumber(Form)
        self.MC_Vol.setObjectName("MC_Vol")
        self.gridLayout.addWidget(self.MC_Vol, 11, 1, 1, 1)
        self.MC_Temp = QtWidgets.QLCDNumber(Form)
        self.MC_Temp.setObjectName("MC_Temp")
        self.gridLayout.addWidget(self.MC_Temp, 11, 3, 1, 1)
        self.MC_State = QtWidgets.QLCDNumber(Form)
        self.MC_State.setObjectName("MC_State")
        self.gridLayout.addWidget(self.MC_State, 11, 4, 1, 1)
        self.Log = QtWidgets.QPlainTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Log.sizePolicy().hasHeightForWidth())
        self.Log.setSizePolicy(sizePolicy)
        self.Log.setObjectName("Log")
        self.gridLayout.addWidget(self.Log, 11, 6, 2, 2)
        self.TSI = QtWidgets.QLabel(Form)
        self.TSI.setObjectName("TSI")
        self.gridLayout.addWidget(self.TSI, 12, 0, 1, 1)
        self.TSI_Vol = QtWidgets.QLCDNumber(Form)
        self.TSI_Vol.setObjectName("TSI_Vol")
        self.gridLayout.addWidget(self.TSI_Vol, 12, 1, 1, 1)
        self.TSI_Temp = QtWidgets.QLCDNumber(Form)
        self.TSI_Temp.setObjectName("TSI_Temp")
        self.gridLayout.addWidget(self.TSI_Temp, 12, 3, 1, 1)
        self.TSI_State = QtWidgets.QLCDNumber(Form)
        self.TSI_State.setObjectName("TSI_State")
        self.gridLayout.addWidget(self.TSI_State, 12, 4, 1, 1)
        self.VSstate = QtWidgets.QLabel(Form)
        self.VSstate.setObjectName("VSstate")
        self.gridLayout.addWidget(self.VSstate, 1, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 5, 0, 1, 8)
        self.VS_State = QtWidgets.QLCDNumber(Form)
        self.VS_State.setObjectName("VS_State")
        self.gridLayout.addWidget(self.VS_State, 1, 1, 1, 1)
        self.Motor = QtWidgets.QLabel(Form)
        self.Motor.setAlignment(QtCore.Qt.AlignCenter)
        self.Motor.setObjectName("Motor")
        self.gridLayout.addWidget(self.Motor, 0, 3, 1, 2)
        self.VSsession = QtWidgets.QLabel(Form)
        self.VSsession.setObjectName("VSsession")
        self.gridLayout.addWidget(self.VSsession, 2, 0, 1, 1)
        self.TSI_T = QtWidgets.QLabel(Form)
        self.TSI_T.setAlignment(QtCore.Qt.AlignCenter)
        self.TSI_T.setObjectName("TSI_T")
        self.gridLayout.addWidget(self.TSI_T, 0, 6, 1, 2)
        self.VS_Time = QtWidgets.QLCDNumber(Form)
        self.VS_Time.setObjectName("VS_Time")
        self.gridLayout.addWidget(self.VS_Time, 3, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 2, 4, 1)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 5, 4, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ThrottleIn.setText(_translate("Form", "Throttle Input"))
        self.TSICurrent.setText(_translate("Form", "Current"))
        self.VSCADA.setText(_translate("Form", "VSCADA"))
        self.Pack2.setText(_translate("Form", "Pack 2"))
        self.MotorTemp.setText(_translate("Form", "Motor Temp"))
        self.ThrottleV.setText(_translate("Form", "Throttle Voltage"))
        self.MotorRPM.setText(_translate("Form", "RPM"))
        self.TSIIMD.setText(_translate("Form", "IMD"))
        self.Voltage.setText(_translate("Form", "Voltage"))
        self.Temp.setText(_translate("Form", "Temp"))
        self.State.setText(_translate("Form", "State"))
        self.SOC.setText(_translate("Form", "SOC"))
        self.Mini_Cell_Voltage.setText(_translate("Form", "Mini Cell Voltage"))
        self.Pack1.setText(_translate("Form", "Pack 1"))
        self.VStime.setText(_translate("Form", "Time"))
        self.Pack3.setText(_translate("Form", "Pack 3"))
        self.Pack4.setText(_translate("Form", "Pack 4"))
        self.MC.setText(_translate("Form", "MC"))
        self.TSI.setText(_translate("Form", "TSI"))
        self.VSstate.setText(_translate("Form", "State"))
        self.Motor.setText(_translate("Form", "Motor Controller"))
        self.VSsession.setText(_translate("Form", "Session"))
        self.TSI_T.setText(_translate("Form", "TSI"))
