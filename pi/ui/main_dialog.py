# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


import picamera
from services.api_service import ApiService

from services.camera_preview import CameraPreview
from services.camera import Camera

from services.db import DB
import json
import sys
import pdb
import requests
import os
import time
from datetime import datetime,tzinfo,timedelta
from datetime import datetime
from dateutil import tz

class MainDialog(QDialog):

    def __init__(self):
        super(MainDialog, self).__init__()
        
        self.api_service = ApiService.getInstance()
        self.db = DB()

        self.user = self.db.get_user()

        if self.user:
            self.first_name = self.user['first_name']
            self.token = self.user['token']
        
        else:
            self.first_name = 'Unnamed User'
            self.token = None
            print('user not found.')        
        
      
        self.latitude = 0 
        self.longitude = 0
        self.gps_time = None
        self.camera = None
        self.camera_test = None
        self.property_id = None
        self.patch_id = None
        self.property_list = None
        
        self.GetPropertyList()
        self.setupUi()
        self.time_synced = False
    
    
    def GetPropertyList(self):
       
        try:
            self.property_list = json.loads(self.user['properties'])
            self.property_id = self.property_list[0]['id']
            self.patch_id = self.property_list[0]['patches'][0]['id']
        except:
            print('Property info not found.')
            
       
        try:
            property_list = self.api_service.property_list(self.token)
            
            if property_list:
                self.property_list = property_list
                self.property_id = self.property_list[0]['id']
                self.patch_id = self.property_list[0]['patches'][0]['id']
                
                self.db.update_properties(json.dumps(self.property_list))
                
        
        except:
            print('Cannot update properties')
    def setGps(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.label_gps.setText( 'lat: '+ str(latitude) + '\nlon: ' + str(longitude) )
        
    def setDateTime(self, t):
        
       
        to_zone = tz.gettz('Australia/Adelaide')
        self.label_datetime.setText('Time: '+ t.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') )
        self.gps_time = t
        if self.time_synced == False:
            self.updateSystemTime()
            self.time_synced = True
            
        
    def updateSystemTime(self):
        clk_id = time.CLOCK_REALTIME
        unix_time = self.gps_time.timestamp()
        
        print(unix_time)
        try:
            time.clock_settime(clk_id, unix_time)
        except:
            print('sudo permission reqired to set syetem time.')
    def setProgress(self, progress):
        self.label_upload.setText(progress)
        
    def setupUi(self):
        
        font = QFont("Arial", 13, QFont.Bold)
        self.setFont(font)    
        self.setObjectName("Dialog")
     
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(150, 100, 220, 55))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(150, 70, 60, 30))
        self.label_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly)
        self.label_2.setObjectName("label_2")
        
        
        
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(150, 170, 180, 30))
        self.label_3.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhFormattedNumbersOnly)
        self.label_3.setObjectName("label_3")
        
        self.comboBox_2 = QtWidgets.QComboBox(self)
        self.comboBox_2.setGeometry(QtCore.QRect(150, 200, 250, 55))
        self.comboBox_2.setObjectName("comboBox2")
        
        self.comboBox_3 = QtWidgets.QComboBox(self)
        self.comboBox_3.setGeometry(QtCore.QRect(450, 200, 250, 55))
        self.comboBox_3.setObjectName("comboBox3")
        
        self.start_button = QtWidgets.QPushButton(self)
        self.start_button.setGeometry(QtCore.QRect(150, 300, 180, 55))
        self.start_button.setObjectName("start_button")

        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setGeometry(QtCore.QRect(350, 300, 180, 55))
        self.stop_button.setObjectName("stop_button")
        
      
        self.start_preview_button = QtWidgets.QPushButton(self)
        self.start_preview_button.setGeometry(QtCore.QRect(150, 380, 180, 55))
        self.start_preview_button.setObjectName("start_preview_button")
        
        self.stop_preview_button = QtWidgets.QPushButton(self)
        self.stop_preview_button.setGeometry(QtCore.QRect(350, 380, 180, 55))
        self.stop_preview_button.setObjectName("stop_preview_button")
        
        self.label_gps = QtWidgets.QLabel(self)
        self.label_gps.setGeometry(QtCore.QRect(150, 450, 400, 60))
        self.label_gps.setObjectName("label_gps")
        
        self.label_datetime = QtWidgets.QLabel(self)
        self.label_datetime.setGeometry(QtCore.QRect(150, 490, 400, 60))
        self.label_datetime.setObjectName("label_datetime")
        
        self.label_upload = QtWidgets.QLabel(self)
        self.label_upload.setGeometry(QtCore.QRect(400, 450, 400, 35))
        self.label_upload.setObjectName("label_upload")
        
        self.label_greeting = QtWidgets.QLabel(self)
        self.label_greeting.setGeometry(QtCore.QRect(150, 30, 200, 25))
        self.label_greeting.setObjectName("label_greeting")
        
        
        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setGeometry(QtCore.QRect(500, 30, 180, 55))
        self.exit_button.setObjectName("exit_button")
        
        
        
        self.preview_label = QtWidgets.QLabel(self)
        self.preview_label.setGeometry(QtCore.QRect(560, 100, 400, 300))
        self.preview_label.setObjectName("preview_label")
        
        
        
        self.retranslateUi()    
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
        self.showFullScreen()

    def update_ui(self):
        self.label_greeting.setText( "Hello, " + self.first_name )
        
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        
        self.label_2.setText(_translate("Dialog", "Interval:"))
        self.label_3.setText(_translate("Dialog", "Property & patch:"))
        self.start_button.setText(_translate("Dialog", "Start"))
        self.stop_button.setText(_translate("Dialog", "Stop"))
       
        self.start_preview_button.setText(_translate("Dialog", "Start preview"))
        self.stop_preview_button.setText(_translate("Dialog", "Stop preview"))
        self.label_gps.setText(_translate("Dialog", "GPS Connecting"))
        self.label_datetime.setText(_translate("Dialog", "Syncing datetime"))
        self.label_upload.setText(_translate("Dialog", "Stating..."))
        
        self.label_greeting.setText(_translate("Dialog", "Hello, " + self.first_name ))
        
       
        
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        
       
        
        self.start_preview_button.clicked.connect(self.start_preview)
        self.stop_preview_button.clicked.connect(self.stop_preview)
        
        self.stop_preview_button.setEnabled(False)
        
      
        
        
        self.exit_button.setText("Close")
        self.exit_button.clicked.connect(self.close_app)
        #self.comboBox.addItem('Every 1 second', 1)
        self.comboBox.addItem('Every 3 seconds', 3)
        self.comboBox.addItem('Every 5 seconds', 5)
        self.comboBox.addItem('Every 10 seconds', 10)
        self.comboBox.addItem('Every 20 seconds', 20)
        self.comboBox.addItem('Every 60 seconds', 60)
            
            
        if self.property_list:
            for i, prop in enumerate(self.property_list):
                self.comboBox_2.addItem(prop['name'], prop['id'])
        
        if self.patch_id:
            for i, patch in enumerate(self.property_list[0]['patches']):
                self.comboBox_3.addItem(patch['name'], patch['id'])
        
        self.comboBox_2.currentIndexChanged.connect(self.propertyChanged)
        self.comboBox_3.currentIndexChanged.connect(self.patchChanged)
        
   

    def propertyChanged(self, value):
        print(value)
        self.property_id = value
    def patchChanged(self, value):
        print(value)
        self.patch_id = value
    
    def start(self):
 
        interval = self.comboBox.currentData()
        print(interval)
               
        try:
               
            self.camera = Camera(self, interval)
            
            self.camera.start()
        except picamera.exc.PiCameraMMALError:
            QMessageBox.warning(self, 'Error', "Camera is in use, please try again later.", QMessageBox.Ok)
            return
            

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
      
    

    def stop(self):
        self.camera.stop()
        del self.camera
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        
    def start_test(self):
        interval = self.comboBox.currentData()
        try:

            self.camera_test = CameraTest(interval)
                    
            self.camera_test.start()
        except picamera.exc.PiCameraMMALError:
                QMessageBox.warning(self, 'Error', "Camera is in use, please try again later.", QMessageBox.Ok)
                return
                
        self.start_test_button.setEnabled(False)
        self.stop_test_button.setEnabled(True)
        
    def stop_test(self):
        self.camera_test.stop()
        del self.camera_test
        
        self.start_test_button.setEnabled(True)
        self.stop_test_button.setEnabled(False)
    

    def close_app(self):
        os._exit(0)
    
    
    def start_preview(self):
        try:

            self.camera_preview = CameraPreview(self)
        
            self.camera_preview.start()
            
        except picamera.exc.PiCameraMMALError:
            QMessageBox.warning(self, 'Error', "Camera is in use, please try again later.", QMessageBox.Ok)
            return
            
        self.start_preview_button.setEnabled(False)
        self.stop_preview_button.setEnabled(True)
        
    def stop_preview(self):
        self.camera_preview.stop()
        del self.camera_preview
        self.preview_label.clear()
        self.start_preview_button.setEnabled(True)
        self.stop_preview_button.setEnabled(False)
    
    def update_preview(self, path):
        if self.camera_preview:
            pixmap = QPixmap(path)
            self.preview_label.setPixmap(pixmap) 
            
            

       





    
