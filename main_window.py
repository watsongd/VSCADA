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
        Form.resize(543, 407)
        Form.setStyleSheet("background : rgb(130, 36, 51)")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.TSI_T = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.TSI_T.setFont(font)
        self.TSI_T.setStyleSheet("color : white")
        self.TSI_T.setAlignment(QtCore.Qt.AlignCenter)
        self.TSI_T.setObjectName("TSI_T")
        self.gridLayout.addWidget(self.TSI_T, 0, 6, 1, 2)
        self.VSstate = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.VSstate.setFont(font)
        self.VSstate.setStyleSheet("color : white")
        self.VSstate.setObjectName("VSstate")
        self.gridLayout.addWidget(self.VSstate, 1, 0, 1, 1)
        self.Mini_Cell_Voltage = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(15)
        self.Mini_Cell_Voltage.setFont(font)
        self.Mini_Cell_Voltage.setStyleSheet("color : white")
        self.Mini_Cell_Voltage.setObjectName("Mini_Cell_Voltage")
        self.gridLayout.addWidget(self.Mini_Cell_Voltage, 6, 7, 1, 1)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setStyleSheet("backgrounf:white;color:white;")
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 5, 4, 1)
        self.Voltage3 = QtWidgets.QLCDNumber(Form)
        self.Voltage3.setStyleSheet("background: white;")
        self.Voltage3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Voltage3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Voltage3.setObjectName("Voltage3")
        self.gridLayout.addWidget(self.Voltage3, 9, 1, 1, 2)
        self.VS_Time = QtWidgets.QLCDNumber(Form)
        self.VS_Time.setStyleSheet("background: white;")
        self.VS_Time.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VS_Time.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.VS_Time.setObjectName("VS_Time")
        self.gridLayout.addWidget(self.VS_Time, 3, 1, 1, 1)
        self.TSIIMD = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.TSIIMD.setFont(font)
        self.TSIIMD.setStyleSheet("color : white")
        self.TSIIMD.setObjectName("TSIIMD")
        self.gridLayout.addWidget(self.TSIIMD, 1, 6, 1, 1)
        self.MotorTemp = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.MotorTemp.setFont(font)
        self.MotorTemp.setStyleSheet("color : white")
        self.MotorTemp.setObjectName("MotorTemp")
        self.gridLayout.addWidget(self.MotorTemp, 2, 3, 1, 1)
        self.VSsession = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.VSsession.setFont(font)
        self.VSsession.setStyleSheet("color : white")
        self.VSsession.setObjectName("VSsession")
        self.gridLayout.addWidget(self.VSsession, 2, 0, 1, 1)
        self.Motor_Throttle = QtWidgets.QLCDNumber(Form)
        self.Motor_Throttle.setStyleSheet("background: white;")
        self.Motor_Throttle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Motor_Throttle.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Motor_Throttle.setObjectName("Motor_Throttle")
        self.gridLayout.addWidget(self.Motor_Throttle, 3, 4, 1, 1)
        self.SOC4 = QtWidgets.QLCDNumber(Form)
        self.SOC4.setStyleSheet("background: white;")
        self.SOC4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SOC4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.SOC4.setObjectName("SOC4")
        self.gridLayout.addWidget(self.SOC4, 10, 6, 1, 1)
        self.State1 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.State1.sizePolicy().hasHeightForWidth())
        self.State1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.State1.setFont(font)
        self.State1.setStyleSheet("background-color : white; color : black;")
        self.State1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.State1.setReadOnly(True)
        self.State1.setObjectName("State1")
        self.gridLayout.addWidget(self.State1, 7, 4, 1, 2)
        self.Temp1 = QtWidgets.QLCDNumber(Form)
        self.Temp1.setStyleSheet("background: white;")
        self.Temp1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Temp1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Temp1.setObjectName("Temp1")
        self.gridLayout.addWidget(self.Temp1, 7, 3, 1, 1)
        self.Motor = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Motor.setFont(font)
        self.Motor.setStyleSheet("color : white")
        self.Motor.setAlignment(QtCore.Qt.AlignCenter)
        self.Motor.setObjectName("Motor")
        self.gridLayout.addWidget(self.Motor, 0, 3, 1, 2)
        self.SOC = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.SOC.setFont(font)
        self.SOC.setStyleSheet("color : white")
        self.SOC.setAlignment(QtCore.Qt.AlignCenter)
        self.SOC.setObjectName("SOC")
        self.gridLayout.addWidget(self.SOC, 6, 6, 1, 1)
        self.TSI_Vol = QtWidgets.QLCDNumber(Form)
        self.TSI_Vol.setStyleSheet("background: white;")
        self.TSI_Vol.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TSI_Vol.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.TSI_Vol.setObjectName("TSI_Vol")
        self.gridLayout.addWidget(self.TSI_Vol, 12, 1, 1, 2)
        self.ThrottleIn = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(15)
        self.ThrottleIn.setFont(font)
        self.ThrottleIn.setStyleSheet("color : white")
        self.ThrottleIn.setObjectName("ThrottleIn")
        self.gridLayout.addWidget(self.ThrottleIn, 3, 3, 1, 1)
        self.Voltage1 = QtWidgets.QLCDNumber(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Voltage1.sizePolicy().hasHeightForWidth())
        self.Voltage1.setSizePolicy(sizePolicy)
        self.Voltage1.setStyleSheet("background: white;")
        self.Voltage1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Voltage1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Voltage1.setObjectName("Voltage1")
        self.gridLayout.addWidget(self.Voltage1, 7, 1, 1, 2)
        self.Voltage = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.Voltage.setFont(font)
        self.Voltage.setStyleSheet("color : white")
        self.Voltage.setAlignment(QtCore.Qt.AlignCenter)
        self.Voltage.setObjectName("Voltage")
        self.gridLayout.addWidget(self.Voltage, 6, 1, 1, 2)
        self.VSCADA = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.VSCADA.setFont(font)
        self.VSCADA.setStyleSheet("color : white")
        self.VSCADA.setAlignment(QtCore.Qt.AlignCenter)
        self.VSCADA.setObjectName("VSCADA")
        self.gridLayout.addWidget(self.VSCADA, 0, 0, 1, 2)
        self.SOC1 = QtWidgets.QLCDNumber(Form)
        self.SOC1.setStyleSheet("background: white;")
        self.SOC1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SOC1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.SOC1.setObjectName("SOC1")
        self.gridLayout.addWidget(self.SOC1, 7, 6, 1, 1)
        self.MC_Temp = QtWidgets.QLCDNumber(Form)
        self.MC_Temp.setStyleSheet("background: white;")
        self.MC_Temp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MC_Temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MC_Temp.setObjectName("MC_Temp")
        self.gridLayout.addWidget(self.MC_Temp, 11, 3, 1, 1)
        self.TSI_State = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TSI_State.sizePolicy().hasHeightForWidth())
        self.TSI_State.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.TSI_State.setFont(font)
        self.TSI_State.setStyleSheet("background-color : white; color : black;")
        self.TSI_State.setText("")
        self.TSI_State.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TSI_State.setReadOnly(True)
        self.TSI_State.setObjectName("TSI_State")
        self.gridLayout.addWidget(self.TSI_State, 12, 4, 1, 2)
        self.SOC2 = QtWidgets.QLCDNumber(Form)
        self.SOC2.setStyleSheet("background: white;")
        self.SOC2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SOC2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.SOC2.setObjectName("SOC2")
        self.gridLayout.addWidget(self.SOC2, 8, 6, 1, 1)
        self.SOC3 = QtWidgets.QLCDNumber(Form)
        self.SOC3.setStyleSheet("background: white;")
        self.SOC3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SOC3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.SOC3.setObjectName("SOC3")
        self.gridLayout.addWidget(self.SOC3, 9, 6, 1, 1)
        self.MC = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.MC.setFont(font)
        self.MC.setStyleSheet("color : white;")
        self.MC.setAlignment(QtCore.Qt.AlignCenter)
        self.MC.setObjectName("MC")
        self.gridLayout.addWidget(self.MC, 11, 0, 1, 1)
        self.MiniCellV1 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV1.setStyleSheet("background: white;")
        self.MiniCellV1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MiniCellV1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MiniCellV1.setObjectName("MiniCellV1")
        self.gridLayout.addWidget(self.MiniCellV1, 7, 7, 1, 1)
        self.TSI_Temp = QtWidgets.QLCDNumber(Form)
        self.TSI_Temp.setStyleSheet("background: white;")
        self.TSI_Temp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TSI_Temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.TSI_Temp.setObjectName("TSI_Temp")
        self.gridLayout.addWidget(self.TSI_Temp, 12, 3, 1, 1)
        self.MiniCellV4 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV4.setStyleSheet("background: white;")
        self.MiniCellV4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MiniCellV4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MiniCellV4.setObjectName("MiniCellV4")
        self.gridLayout.addWidget(self.MiniCellV4, 10, 7, 1, 1)
        self.Pack2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Pack2.setFont(font)
        self.Pack2.setStyleSheet("color : white;")
        self.Pack2.setAlignment(QtCore.Qt.AlignCenter)
        self.Pack2.setObjectName("Pack2")
        self.gridLayout.addWidget(self.Pack2, 8, 0, 1, 1)
        self.MC_State = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MC_State.sizePolicy().hasHeightForWidth())
        self.MC_State.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.MC_State.setFont(font)
        self.MC_State.setStyleSheet("background-color : white; color : black;")
        self.MC_State.setText("")
        self.MC_State.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.MC_State.setReadOnly(True)
        self.MC_State.setObjectName("MC_State")
        self.gridLayout.addWidget(self.MC_State, 11, 4, 1, 2)
        self.Voltage2 = QtWidgets.QLCDNumber(Form)
        self.Voltage2.setStyleSheet("background: white;")
        self.Voltage2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Voltage2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Voltage2.setObjectName("Voltage2")
        self.gridLayout.addWidget(self.Voltage2, 8, 1, 1, 2)
        self.MiniCellV3 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV3.setStyleSheet("background: white;")
        self.MiniCellV3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MiniCellV3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MiniCellV3.setObjectName("MiniCellV3")
        self.gridLayout.addWidget(self.MiniCellV3, 9, 7, 1, 1)
        self.State2 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.State2.sizePolicy().hasHeightForWidth())
        self.State2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.State2.setFont(font)
        self.State2.setStyleSheet("background-color : white; color : black;")
        self.State2.setText("")
        self.State2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.State2.setReadOnly(True)
        self.State2.setObjectName("State2")
        self.gridLayout.addWidget(self.State2, 8, 4, 1, 2)
        self.MiniCellV2 = QtWidgets.QLCDNumber(Form)
        self.MiniCellV2.setStyleSheet("background: white;")
        self.MiniCellV2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MiniCellV2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MiniCellV2.setObjectName("MiniCellV2")
        self.gridLayout.addWidget(self.MiniCellV2, 8, 7, 1, 1)
        self.Pack4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Pack4.setFont(font)
        self.Pack4.setStyleSheet("color : white;")
        self.Pack4.setAlignment(QtCore.Qt.AlignCenter)
        self.Pack4.setObjectName("Pack4")
        self.gridLayout.addWidget(self.Pack4, 10, 0, 1, 1)
        self.Voltage4 = QtWidgets.QLCDNumber(Form)
        self.Voltage4.setStyleSheet("background: white;")
        self.Voltage4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Voltage4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Voltage4.setObjectName("Voltage4")
        self.gridLayout.addWidget(self.Voltage4, 10, 1, 1, 2)
        self.Temp4 = QtWidgets.QLCDNumber(Form)
        self.Temp4.setStyleSheet("background: white;")
        self.Temp4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Temp4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Temp4.setObjectName("Temp4")
        self.gridLayout.addWidget(self.Temp4, 10, 3, 1, 1)
        self.Temp3 = QtWidgets.QLCDNumber(Form)
        self.Temp3.setStyleSheet("background: white;")
        self.Temp3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Temp3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Temp3.setObjectName("Temp3")
        self.gridLayout.addWidget(self.Temp3, 9, 3, 1, 1)
        self.Temp2 = QtWidgets.QLCDNumber(Form)
        self.Temp2.setStyleSheet("background: white;")
        self.Temp2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Temp2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Temp2.setObjectName("Temp2")
        self.gridLayout.addWidget(self.Temp2, 8, 3, 1, 1)
        self.MC_Vol = QtWidgets.QLCDNumber(Form)
        self.MC_Vol.setStyleSheet("background: white;")
        self.MC_Vol.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.MC_Vol.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.MC_Vol.setObjectName("MC_Vol")
        self.gridLayout.addWidget(self.MC_Vol, 11, 1, 1, 2)
        self.State3 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.State3.sizePolicy().hasHeightForWidth())
        self.State3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.State3.setFont(font)
        self.State3.setStyleSheet("background-color : white; color : black;")
        self.State3.setText("")
        self.State3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.State3.setReadOnly(True)
        self.State3.setObjectName("State3")
        self.gridLayout.addWidget(self.State3, 9, 4, 1, 2)
        self.Log = QtWidgets.QPlainTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Log.sizePolicy().hasHeightForWidth())
        self.Log.setSizePolicy(sizePolicy)
        self.Log.setStyleSheet("background-color : white; color : black;")
        self.Log.setPlainText("")
        self.Log.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.Log.setObjectName("Log")
        self.gridLayout.addWidget(self.Log, 11, 6, 2, 2)
        self.VS_State = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VS_State.sizePolicy().hasHeightForWidth())
        self.VS_State.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.VS_State.setFont(font)
        self.VS_State.setStyleSheet("background-color : white; color : black;")
        self.VS_State.setText("")
        self.VS_State.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.VS_State.setReadOnly(True)
        self.VS_State.setObjectName("VS_State")
        self.gridLayout.addWidget(self.VS_State, 1, 1, 1, 1)
        self.VStime = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.VStime.setFont(font)
        self.VStime.setStyleSheet("color : white")
        self.VStime.setObjectName("VStime")
        self.gridLayout.addWidget(self.VStime, 3, 0, 1, 1)
        self.Motor_Temp = QtWidgets.QLCDNumber(Form)
        self.Motor_Temp.setStyleSheet("background: white;")
        self.Motor_Temp.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Motor_Temp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Motor_Temp.setObjectName("Motor_Temp")
        self.gridLayout.addWidget(self.Motor_Temp, 2, 4, 1, 1)
        self.State4 = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.State4.sizePolicy().hasHeightForWidth())
        self.State4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(".SF NS Text")
        font.setPointSize(20)
        self.State4.setFont(font)
        self.State4.setStyleSheet("background-color : white; color : black;")
        self.State4.setText("")
        self.State4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.State4.setReadOnly(True)
        self.State4.setObjectName("State4")
        self.gridLayout.addWidget(self.State4, 10, 4, 1, 2)
        self.Pack1 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Pack1.setFont(font)
        self.Pack1.setStyleSheet("color : white;")
        self.Pack1.setAlignment(QtCore.Qt.AlignCenter)
        self.Pack1.setObjectName("Pack1")
        self.gridLayout.addWidget(self.Pack1, 7, 0, 1, 1)
        self.Motor_RPM = QtWidgets.QLCDNumber(Form)
        self.Motor_RPM.setStyleSheet("background: white;")
        self.Motor_RPM.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Motor_RPM.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.Motor_RPM.setObjectName("Motor_RPM")
        self.gridLayout.addWidget(self.Motor_RPM, 1, 4, 1, 1)
        self.VS_Session = QtWidgets.QLCDNumber(Form)
        self.VS_Session.setStyleSheet("background: white;")
        self.VS_Session.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VS_Session.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.VS_Session.setObjectName("VS_Session")
        self.gridLayout.addWidget(self.VS_Session, 2, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setStyleSheet("backgrounf:white;color:white;")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 2, 4, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setStyleSheet("backgrounf:white;color:white;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 5, 0, 1, 8)
        self.Pack3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Pack3.setFont(font)
        self.Pack3.setStyleSheet("color : white;")
        self.Pack3.setAlignment(QtCore.Qt.AlignCenter)
        self.Pack3.setObjectName("Pack3")
        self.gridLayout.addWidget(self.Pack3, 9, 0, 1, 1)
        self.MotorRPM = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.MotorRPM.setFont(font)
        self.MotorRPM.setStyleSheet("color : white")
        self.MotorRPM.setObjectName("MotorRPM")
        self.gridLayout.addWidget(self.MotorRPM, 1, 3, 1, 1)
        self.TSI_IMD = QtWidgets.QLCDNumber(Form)
        self.TSI_IMD.setStyleSheet("background: white;")
        self.TSI_IMD.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TSI_IMD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.TSI_IMD.setObjectName("TSI_IMD")
        self.gridLayout.addWidget(self.TSI_IMD, 1, 7, 1, 1)
        self.State = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.State.setFont(font)
        self.State.setStyleSheet("color : white")
        self.State.setAlignment(QtCore.Qt.AlignCenter)
        self.State.setObjectName("State")
        self.gridLayout.addWidget(self.State, 6, 4, 1, 2)
        self.Temp = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.Temp.setFont(font)
        self.Temp.setStyleSheet("color : white")
        self.Temp.setAlignment(QtCore.Qt.AlignCenter)
        self.Temp.setObjectName("Temp")
        self.gridLayout.addWidget(self.Temp, 6, 3, 1, 1)
        self.TSI = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.TSI.setFont(font)
        self.TSI.setStyleSheet("color : white;")
        self.TSI.setAlignment(QtCore.Qt.AlignCenter)
        self.TSI.setObjectName("TSI")
        self.gridLayout.addWidget(self.TSI, 12, 0, 1, 1)
        self.TSICurrent = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(16)
        self.TSICurrent.setFont(font)
        self.TSICurrent.setStyleSheet("color : white")
        self.TSICurrent.setObjectName("TSICurrent")
        self.gridLayout.addWidget(self.TSICurrent, 2, 6, 1, 1)
        self.ThrottleV = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Hoefler Text")
        font.setPointSize(15)
        self.ThrottleV.setFont(font)
        self.ThrottleV.setStyleSheet("color : white")
        self.ThrottleV.setObjectName("ThrottleV")
        self.gridLayout.addWidget(self.ThrottleV, 3, 6, 1, 1)
        self.TSI_Current = QtWidgets.QLCDNumber(Form)
        self.TSI_Current.setStyleSheet("background: white;")
        self.TSI_Current.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TSI_Current.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.TSI_Current.setObjectName("TSI_Current")
        self.gridLayout.addWidget(self.TSI_Current, 2, 7, 1, 1)
        self.TSI_Throttle_V = QtWidgets.QLCDNumber(Form)
        self.TSI_Throttle_V.setStyleSheet("background: white;")
        self.TSI_Throttle_V.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TSI_Throttle_V.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.TSI_Throttle_V.setObjectName("TSI_Throttle_V")
        self.gridLayout.addWidget(self.TSI_Throttle_V, 3, 7, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TSI_T.setText(_translate("Form", "TSI"))
        self.VSstate.setText(_translate("Form", "State"))
        self.Mini_Cell_Voltage.setText(_translate("Form", "Mini Cell(V)"))
        self.TSIIMD.setText(_translate("Form", "IMD"))
        self.MotorTemp.setText(_translate("Form", "Temp(°F)"))
        self.VSsession.setText(_translate("Form", "Session"))
        self.State1.setText(_translate("Form", "state1"))
        self.Motor.setText(_translate("Form", "Motor"))
        self.SOC.setText(_translate("Form", "SOC(%)"))
        self.ThrottleIn.setText(_translate("Form", "Throttle(V)"))
        self.Voltage.setText(_translate("Form", "Voltage(V)"))
        self.VSCADA.setText(_translate("Form", "VSCADA"))
        self.MC.setText(_translate("Form", "MC"))
        self.Pack2.setText(_translate("Form", "Pack 2"))
        self.Pack4.setText(_translate("Form", "Pack 4"))
        self.VStime.setText(_translate("Form", "Time"))
        self.Pack1.setText(_translate("Form", "Pack 1"))
        self.Pack3.setText(_translate("Form", "Pack 3"))
        self.MotorRPM.setText(_translate("Form", "Speed(rpm)"))
        self.State.setText(_translate("Form", "State"))
        self.Temp.setText(_translate("Form", "Temp(°C)"))
        self.TSI.setText(_translate("Form", "TSI"))
        self.TSICurrent.setText(_translate("Form", "Current(A)"))
        self.ThrottleV.setText(_translate("Form", "Throttle(V)"))

