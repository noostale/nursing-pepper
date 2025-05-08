#!/usr/bin/env python
# -*- coding: utf-8 -*-
# animations
# http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper

# How to use

# export PEPPER_IP=<...>
# python
# >>> import pepper_cmd
# >>> from pepper_cmd import *
# >>> begin()
# >>> pepper_cmd.robot.<fn>()
# >>> end()

import time
import os
import socket
import threading
import math
import random
import datetime
from datetime import datetime
import pyttsx3
import csv


import qi
from naoqi import ALProxy

# Python Image Library
from PIL import Image

laserValueList = [
  # RIGHT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Right/Horizontal/Seg15/Y/Sensor/Value",
  # FRONT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg15/Y/Sensor/Value",
  # LEFT LASER
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg01/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg01/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg02/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg02/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg03/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg03/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg04/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg04/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg05/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg05/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg06/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg06/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg07/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg07/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg08/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg08/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg09/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg09/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg10/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg10/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg11/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg11/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg12/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg12/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg13/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg13/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg14/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg14/Y/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg15/X/Sensor/Value",
  "Device/SubDeviceList/Platform/LaserSensor/Left/Horizontal/Seg15/Y/Sensor/Value"
]


app = None
session = None
tts_service = None
memory_service = None
motion_service = None
anspeech_service = None
tablet_service = None

robot = None        # PepperRobot object

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# Sensors
headTouch = 0.0
handTouch = [0.0, 0.0] # left, right
sonar = [0.0, 0.0] # front, back


# Sensors

def sensorThread(robot):
    sonarValues = ["Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value",
                  "Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"]
    headTouchValue = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
    handTouchValues = [ "Device/SubDeviceList/LHand/Touch/Back/Sensor/Value",
                   "Device/SubDeviceList/RHand/Touch/Back/Sensor/Value" ]
    frontLaserValues = [ 
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/Y/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/Y/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/X/Sensor/Value",
      "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/Y/Sensor/Value" ]
 
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        robot.headTouch = robot.memory_service.getData(headTouchValue)
        robot.handTouch = robot.memory_service.getListData(handTouchValues)
        robot.sonar = robot.memory_service.getListData(sonarValues)
        laserValues = robot.memory_service.getListData(frontLaserValues)
        dd = 0 # average distance
        c = 0        
        for i in range(0,len(laserValues),2):
            px = laserValues[i] if laserValues[i] is not None else 10
            py = laserValues[i+1] if laserValues[i+1] is not None else 0
            d = math.sqrt(px*px+py*py)
            if d<10:
                dd = dd + d
                c = c+1
        
        if (c>0):
            robot.frontlaser = dd / c
        else:
            robot.frontlaser = 10.0

        #print "Head touch middle value=", robot.headTouch
        #print "Hand touch middle value=", robot.handTouch
        #print "Sonar [Front, Back]", robot.sonar
        time.sleep(0.2)
    #print "Exiting Thread"




def touchcb(value):
    print "value=",value

    touched_bodies = []
    for p in value:
        if p[1]:
            touched_bodies.append(p[0])

    print touched_bodies

asr_word = ''
asr_confidence = 0
asr_timestamp = 0

def onWordRecognized(value):
    global asr_word, asr_confidence, asr_timestamp
    print "ASR value = ",value,time.time()
    if (value[1]>0 and value[0]!=''):
    #if (value[1]>0 and (value[0]!='' or time.time()-asr_timestamp>1.0)):
    #if (value[1]>0):
        asr_word = value[0]
        asr_confidence = value[1]
        asr_timestamp = time.time()

def sensorvalue(sensorname):
    global robot
    if (robot!=None):
        return robot.sensorvalue(sensorname)


touchcnt = 0

# function called when the signal onTouchDown is triggered
def touch_cb(x, y):
    global robot, touchcnt
    print "Touch coordinates are x: ", x, " y: ", y
    robot.screenTouch = (x,y)
    touchcnt = touchcnt + 1
    time.sleep(1)
    touchcnt = touchcnt - 1
    if touchcnt == 0:
        robot.screenTouch = (0.0,0.0)



def laserMonitorThread (memory_service):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        laserValues =  memory_service.getListData(laserValueList)
        #print laserValues[44],laserValues[45] #X,Y values of central point
        time.sleep(0.2)
    print "Exiting Thread"


# Begin/end

def begin():
    global robot
    print 'begin'
    if (robot==None):
        robot=PepperRobot()
        robot.connect()
    robot.begin()

def end():
    global robot
    print 'end'
    time.sleep(0.5) # make sure stuff ends
    if (robot!=None):
        robot.quit()


# Robot motion

def stop():
    global robot
    if (robot==None):
        begin()
    robot.stop()

def forward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.forward(r)

def backward(r=1):
    global robot
    if (robot==None):
        begin()
    robot.backward(r)

def left(r=1):
    global robot
    if (robot==None):
        begin()
    robot.left(r)

def right(r=1):
    global robot
    if (robot==None):
        begin()
    robot.right(r)

def robot_stop_request(): # stop until next begin()
    if (robot!=None):
        robot.stop_request = True
        robot.stop()
        print("stop request")



# Wait

def wait(r=1):
    print 'wait',r
    for i in range(0,r):
        time.sleep(3)


# Sounds

def bip(r=1):
    print 'bip'


def bop(r=1):
    print 'bop'


# Speech

def say(strsay):
    global robot
    print 'Say ',strsay
    if (robot==None):
        begin()
    robot.say(strsay)

def asay(strsay):
    global robot
    print 'Animated Say ',strsay
    if (robot==None):
        begin()
    robot.asay(strsay)



# Other 

# Alive behaviors
def setAlive(alive):
    global robot
    robot.setAlive(alive)

def stand():
    global robot
    robot.stand()

def disabled():
    global robot
    robot.disabled()

def interact():
    global robot
    robot.interactive()


def showurl(url):
    global robot
    if (robot!=None):
        return robot.showurl(url)


def run_behavior(bname):
    global session
    beh_service = session.service("ALBehaviorManager")
    beh_service.startBehavior(bname)
    #time.sleep(10)
    #beh_service.stopBehavior(bname)


def takephoto():
    global robot
    robot.takephoto()


def opendiag():
    global robot
    robot.introduction()

def sax():
    global robot
    robot.sax()


class PepperRobot:

    def __init__(self):
        self.isConnected = False
        # Sensors
        self.headTouch = 0.0
        self.handTouch = [0.0, 0.0] # left, right
        self.sonar = [0.0, 0.0] # front, back
        self.frontlaser = 0.0
        self.screenTouch = (0,0)
        self.language = "English"
        self.stop_request = False
        self.frame_grabber = False
        self.face_detection = False
        self.got_face = False

        self.FER_server_IP = None
        self.FER_server_port = 5678

        self.logfile = None

        self.sensorThread = None
        self.laserThread = None
        self.lthr = None # log thread

        self.jointNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]

        self.fakeASRkey = 'FakeRobot/ASR'
        self.fakeASRtimekey = 'FakeRobot/ASRtime'


    def session_service(self,name):
        try:
            return self.session.service(name)
        except:
            print("Service %s not available." %(name))
            return None


        # Connect to the robot
    def connect(self, pip=os.environ.get('PEPPER_IP'),
                      pport=None,
                      alive=False):
        # Resolve IP/port
        self.ip = pip
        if pport is not None:
            self.port = pport
        elif 'PEPPER_PORT' in os.environ:
            self.port = int(os.environ['PEPPER_PORT'])
        else:
            self.port = 9559

        if self.isConnected:
            print "Robot already connected."
            return

        print "Connecting to robot %s:%d ..." % (self.ip, self.port)
        try:
            connection_url = "tcp://%s:%d" % (self.ip, self.port)
            self.app = qi.Application(["Pepper command",
                                       "--qi-url=" + connection_url])
            self.app.start()
        except RuntimeError:
            print ("%sCannot connect to Naoqi at %s:%d %s"
                   % (RED, self.ip, self.port, RESET))
            return

        print ("%sConnected to robot %s:%d %s"
               % (GREEN, self.ip, self.port, RESET))
        self.session = self.app.session

        # List all the services you want, mapped to your attribute names
        service_map = {
            'memory_service':           'ALMemory',
            'motion_service':           'ALMotion',
            'tts_service':              'ALTextToSpeech',
            'anspeech_service':         'ALAnimatedSpeech',
            'leds_service':             'ALLeds',
            'asr_service':              'ALSpeechRecognition',
            'tablet_service':           'ALTabletService',
            'touch_service':            'ALTouch',
            'animation_player_service': 'ALAnimationPlayer',
            'beh_service':              'ALBehaviorManager',
            'al_service':               'ALAutonomousLife',
            'rp_service':               'ALRobotPosture',
            'bm_service':               'ALBackgroundMovement',
            'ba_service':               'ALBasicAwareness',
            'sm_service':               'ALSpeakingMovement',
            'audiorec_service':         'ALAudioRecorder',
            'audio_service':            'ALAudioDevice',
            'battery_service':          'ALBattery',
            'people_service':           'ALPeoplePerception',
        }

        print "Starting services..."
        for attr, serv_name in service_map.items():
            try:
                setattr(self, attr, self.session.service(serv_name))
            except RuntimeError:
                setattr(self, attr, None)
                print "  - %s not available." % serv_name

        # Enable autonomous life if requested
        if self.bm_service:
            self.alive = alive
            print "Alive behaviors: %r" % self.alive
            self.bm_service.setEnabled(self.alive)
            if self.ba_service: self.ba_service.setEnabled(self.alive)
            if self.sm_service: self.sm_service.setEnabled(self.alive)

        # If the tablet is there, hook up touch callbacks
        if self.tablet_service and self.touch_service:
            webview = "http://198.18.0.1/apps/spqrel/index.html"
            self.tablet_service.showWebview(webview)
            self.touchsignalID = \
                self.tablet_service.onTouchDown.connect(touch_cb)
            self.touchstatus = self.touch_service.getStatus()
            self.touchsensorlist = self.touch_service.getSensorList()

        self.isConnected = True
        print "Connection complete."


    def quit(self):
        print "Quit Pepper robot."
        self.sensorThread = None
        self.laserThread = None
        if self.sensorThread != None:
            self.sensorThread.do_run = False
            self.sensorThread = None
        if self.laserThread != None:
            self.laserThread.do_run = False
            self.laserThread = None
        
        if self.session!=None and self.tablet_service!=None:
            self.tablet_service.onTouchDown.disconnect(self.touchsignalID)
        time.sleep(1)
        self.app.stop()
        

    # general commands

    def begin(self):
        self.stop_request = False
        self.ears_led(False)
        self.white_eyes()

    def exec_cmd(self, params):
        cmdstr = "self."+params
        print "Executing %s" %(cmdstr)
        eval(cmdstr)    

    def tablet_home(self):
        webview = "http://198.18.0.1/apps/spqrel/index.html"
        self.tablet_service.showWebview(webview)


    def print_available_services(self):
        """
        Print all ALProxy services currently initialized on the robot.
        Call begin() first to ensure the robot is connected.
        """
        global robot

        if robot is None or not getattr(robot, 'session', None):
            print "Robot not connected. Please call begin() first."
            return

        print "Available services:"
        for attr in dir(robot):
            if attr.endswith('_service'):
                svc = getattr(robot, attr)
                if svc is not None:
                    print '  - %s: %s' % (attr, svc)



    # Network

    def networkstatus(self):
        # TODO
        #self.tablet_service.configureWifi(const std::string& security, const std::string& ssid, const std::string& key)
        #connectWifi(const std::string& ssid)
        return self.tablet_service.getWifiStatus()


    def robotIp(self):
        return self.tablet_service.robotIp() # just tablet IP ...

    # Leds

    def white_eyes(self):
        # white face leds
        self.leds_service.on('FaceLeds')


    def green_eyes(self):
        if self.leds_service!=None:
            # green face leds
            self.leds_service.on('LeftFaceLedsGreen')
            self.leds_service.off('LeftFaceLedsRed')
            self.leds_service.off('LeftFaceLedsBlue')
            self.leds_service.on('RightFaceLedsGreen')
            self.leds_service.off('RightFaceLedsRed')
            self.leds_service.off('RightFaceLedsBlue')

    def red_eyes(self):
        if self.leds_service!=None:
            # red face leds
            self.leds_service.off('LeftFaceLedsGreen')
            self.leds_service.on('LeftFaceLedsRed')
            self.leds_service.off('LeftFaceLedsBlue')
            self.leds_service.off('RightFaceLedsGreen')
            self.leds_service.on('RightFaceLedsRed')
            self.leds_service.off('RightFaceLedsBlue')

    def blue_eyes(self):
        if self.leds_service!=None:
            # red face leds
            self.leds_service.off('LeftFaceLedsGreen')
            self.leds_service.off('LeftFaceLedsRed')
            self.leds_service.on('LeftFaceLedsBlue')
            self.leds_service.off('RightFaceLedsGreen')
            self.leds_service.off('RightFaceLedsRed')
            self.leds_service.on('RightFaceLedsBlue')


    def ears_led(self, enable):
        # Ears leds
        if enable:
            self.leds_service.on('EarLeds')
        else:
            self.leds_service.off('EarLeds')


    # Touch/distance sensors

    def startSensorMonitor(self):
        if self.sensorThread == None:
            # create a thead that monitors directly the signal
            self.sensorThread = threading.Thread(target = sensorThread, args = (self, ))
            self.sensorThread.start()
            time.sleep(0.5)

    def stopSensorMonitor(self):
        self.sensorThread.do_run = False
        self.sensorThread = None


    # Laser

    def startLaserMonitor(self):
        if self.laserThread==None:
            #create a thead that monitors directly the signal
            self.laserThread = threading.Thread(target = laserMonitorThread, args = (self.memory_service,))
            self.laserThread.start()

    def stopLaserMonitor(self):
        self.laserThread.do_run = False
        self.laserThread = None


    # Camera

    def startFrameGrabber(self):
        # Connect to camera
        self.camProxy = ALProxy("ALVideoDevice", self.ip, self.port)
        resolution = 2    # VGA
        colorSpace = 11   # RGB
        # self.videoClient = self.camProxy.subscribe("grab3_images", resolution, colorSpace, 5)
        self.videoClient = self.camProxy.subscribeCamera("grab3_images", 0, resolution, colorSpace, 5)
        self.frame_grabber = True

    def stopFrameGrabber(self):
        # Connect to camera
        self.camProxy.unsubscribe(self.videoClient)
        self.frame_grabber = False

    def sendImage(self, ip, port):
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        img = self.camProxy.getImageRemote(self.videoClient)

        if img is None:
            return 'ERROR'

        # Get the image size and pixel array.
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)

        # Convert to grayscale
        img = imx.convert('L')   
        aimg = img.tobytes()

        #print("Connecting to %s:%d ..." %(ip,port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))
            #print("OK")

            #print("Sending image ...")
            #print("Image size: %d %d" %(imageWidth * imageHeight, len(aimg)))

            msg = '%9d\n' %len(aimg)
            s.send(msg.encode())
            s.send(aimg)

            data = s.recv(80)
            rcv_msg = data.decode()
            #print("Reply: %s" %rcv_msg)

            s.close()
            #print("Connection closed ")
            return rcv_msg
        except:
            print("Send image: connection error")
            return 'ERROR'

    def saveImage(self, filename):

        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        img = self.camProxy.getImageRemote(self.videoClient)

        # Get the image size and pixel array.
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)

        # Save the image.
        imx.save(filename, "PNG")


    def startFaceDetection(self):
        if self.face_detection:  # already active
            return

        # Connect to camera
        self.startFrameGrabber()

        # Connect the event callback.
        self.frsub = self.memory_service.subscriber("FaceDetected")
        self.ch1 = self.frsub.signal.connect(self.on_facedetected)
        self.got_face = False
        self.savedfaces = []
        self.face_detection = True
        self.face_recording = False # if images are saved on file

    def stopFaceDetection(self):
        self.frsub.signal.disconnect(self.ch1)
        self.camProxy.unsubscribe(self.videoClient)
        self.face_recording = False
        self.face_detection = False
        self.white_eyes()

    def setFaceRecording(self,enable):
         self.face_recording = enable

    def on_facedetected(self, value):
        """
        Callback for event FaceDetected.
        """
        faceID = -1

        if value == []:  # empty value when the face disappears
            self.got_face = False
            self.facetimeStamp = None
            self.white_eyes()
            self.memset('facedetected', 'false')
        elif not self.got_face:  # only the first time a face appears
            self.got_face = True
            self.green_eyes()
            self.memset('facedetected', 'true')

            #print "I saw a face!"
            #self.tts.say("Hello, you!")
            self.facetimeStamp = time.time() #value[0]
            #print "TimeStamp is: " + str(self.facetimeStamp)

            # Second Field = array of face_Info's.
            faceInfoArray = value[1]
            for j in range( len(faceInfoArray)-1 ):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]

                faceID = faceExtraInfo[0]

                #print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                #print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                #print "Face Extra Infos :" + str(faceExtraInfo)

                #print "Face ID: %d" %faceID

        if self.camProxy!=None and faceID>=0 and faceID not in self.savedfaces and self.face_recording:
            # Get the image
            img = self.camProxy.getImageRemote(self.videoClient)

            # Get the image size and pixel array.
            imageWidth = img[0]
            imageHeight = img[1]
            array = img[6]

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

            # Save the image.
            fname = "face_%03d.png" %faceID
            im.save(fname, "PNG")
            print "Image face %d saved." %faceID

            self.savedfaces.append(faceID)

    # Time of continuous face detection
    def faceDetectionTime(self):
        if self.facetimeStamp is not None:
            return time.time() - self.facetimeStamp
        else:
            return 0

    # Audio settings

    def getVolume(self):
        return self.audio_service.getOutputVolume()

    def setVolume(self, v):
        self.audio_service.setOutputVolume(v)


    def timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    # Audio recording

    def startAudioRecording(self):
        audiofile = '/home/nao/audio/audiorec_%s.wav' %(datetime.now().strftime("%Y%m%d_%H%M%S"))

        # Configures the channels that need to be recorded.
        channels = [0,0,1,0]  # Left, Right, Front, Rear
        self.audiorec_service.startMicrophonesRecording(audiofile, 'wav', 16000, channels)
        self.ears_led(True)

    def stopAudioRecording(self):
        self.audiorec_service.stopMicrophonesRecording()
        self.ears_led(False)



    # Speech

    # English, Italian, French
    def setLanguage(self, lang):
        languages = {"en" : "English", "it": "Italian"}
        if  (lang in languages.keys()):
            lang = languages[lang]
        self.tts_service.setLanguage(lang)

    def tts(self, interaction):
        if self.stop_request:
            return
        
        


        self.tts_service.setParameter("speed", 80)
        self.tts_service.say(interaction)
        

    def say(self, interaction):
        if self.stop_request:
            return
        print('Say: %s' %interaction)
        if self.tts_service!=None:
            
            self.tts_service.setParameter("speed", 80)
            self.asay2(interaction)
 
    def asay2(self, interaction):
        if self.stop_request:
            return
        if self.anspeech_service!=None:
            # set the local configuration
            configuration = {"bodyLanguageMode":"contextual"}
            self.anspeech_service.say(interaction, configuration)

    def asay(self, interaction):
        if self.stop_request:
            return
        if self.anspeech_service is None:
            return

        # set the local configuration
        #configuration = {"bodyLanguageMode":"contextual"}

        # http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer-advanced.html#animationplayer-list-behaviors-pepper
        vanim = ["animations/Stand/Gestures/Enthusiastic_4",
                 "animations/Stand/Gestures/Enthusiastic_5",
                 "animations/Stand/Gestures/Excited_1",
                 "animations/Stand/Gestures/Explain_1" ]
        anim = random.choice(vanim) # random animation

        if ('hello' in interaction):
            anim = "animations/Stand/Gestures/Hey_1"
    
        self.anspeech_service.say("^start("+anim+") " + interaction+" ^wait("+anim+")")

    def reset_fake_asr(self):
        self.memory_service.insertData(self.fakeASRkey,'')

    def fake_asr(self):
        global asr_word, asr_confidence, asr_timestamp
        try:
            r = self.memory_service.getData(self.fakeASRkey)
            if r!='':
                asr_word = r
                asr_confidence = 1.0
                asr_timestamp = self.memory_service.getData(self.fakeASRtimekey)
                print('fake ASR: [%s], %r' %(asr_word,asr_timestamp))
                self.reset_fake_asr()
        except:
            pass

    def asr_cancel(self):
        self.asr_cancel_flag = True

    # vocabulary = list of keywords, e.g. ["yes", "no", "please"]
    # blocking until timeout
    def asr(self, vocabulary, timeout=5):
        global asr_word, asr_confidence, asr_timestamp
        #establishing vocabulary
        if (self.asr_service != None):
            self.asr_service.pause(True)
            self.asr_service.setVocabulary(vocabulary, False)
            self.asr_service.pause(False)
            # Start the speech recognition engine with user Test_ASR
            self.asr_service.subscribe("asr_pepper_cmd")
            print 'Speech recognition engine started'

            #subscribe to event WordRecognized
            subWordRecognized = self.memory_service.subscriber("WordRecognized")
            idSubWordRecognized = subWordRecognized.signal.connect(onWordRecognized)
        else:
            print('ASR service not available. Use %s memory key to say something' %self.fakeASRkey)
            self.reset_fake_asr()
            #val = raw_input('Enter ASR text: ')
            #return val


        self.asr_cancel_flag = False
        asr_word = ''
        i = 0
        dt = 0.5
        while ((timeout<0 or i<timeout) and asr_word=='' and not self.asr_cancel_flag):
            self.fake_asr()
            time.sleep(dt)
            i += dt

        if (self.asr_service != None):
            #Disconnecting callbacks and subscribers
            self.asr_service.unsubscribe("asr_pepper_cmd")
            subWordRecognized.signal.disconnect(idSubWordRecognized)

        

        dt = time.time() - asr_timestamp

        print("dt %r %r  -  %f %f" %(time.time(),asr_timestamp, dt, timeout))

        if ((timeout<0 or dt<timeout) and asr_confidence>0.3):
            print("ASR: %s" %asr_word)
            return asr_word
        else:
            print("ASR: none")
            return ''


    def bip(self, r=1):
        print 'bip -- NOT IMPLEMENTED'


    def bop(self, r=1):
        print 'bop -- NOT IMPLEMENTED'


    # animations/Stand/Gestures/
    # Please_1
    # Hey_1; Hey_3; Hey_4
    def animation(self, interaction):
        
        print '[DEBUG] raw ->', repr(interaction)
        
        interaction = interaction.strip()
        
        print '[DEBUG] raw ->', repr(interaction)
        
        if self.stop_request:
            return
        if interaction[0:4]!='anim':
            interaction = 'animations/Stand/Gestures/' + interaction
        print 'Animation ',interaction
        if self.animation_player_service:
            self.animation_player_service.run(interaction)
        else:
            beh = self.session.service("ALBehaviorManager")
            beh.runBehavior(interaction)




    # Alive behaviors

    def setAlive(self, alive):
        if self.bm_service!=None:
            self.alive = alive
            print('Alive behaviors: %r' %self.alive)
            self.bm_service.setEnabled(self.alive)
            self.ba_service.setEnabled(self.alive)
            self.sm_service.setEnabled(self.alive)

    # Tablet

    def showurl(self, weburl):
        if self.tablet_service!=None:
            if weburl[0:4]!='http':
                weburl = "http://198.18.0.1/apps/spqrel/%s" %(weburl)
            print("URL: %s" %weburl)
            if weburl[-3:]=='jpg' or weburl[-3:]=='png':
                self.tablet_service.showImage(weburl)
            else:
                self.tablet_service.showWebview(weburl)


    # Robot motion

    def stop(self):
        print 'stop'
        self.motion_service.stopMove()
        if self.beh_service!=None:
            bns = self.beh_service.getRunningBehaviors()
            for b in bns:
                self.beh_service.stopBehavior(b)

    def forward(self, r=100):
        if self.stop_request:
            return
        print 'forward',r
        x = r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def backward(self, r=1):
        if self.stop_request:
            return
        print 'backward',r
        x = -r
        y = 0.0
        theta = 0.0
        self.motion_service.moveTo(x, y, theta) #blocking function

    def left(self, r=1):
        if self.stop_request:
            return
        print 'left',r
        #Turn 90deg to the left
        x = 0.0
        y = 0.0
        theta = math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    def right(self, r=1):
        if self.stop_request:
            return
        print 'right',r
        #Turn 90deg to the right
        x = 0.0
        y = 0.0
        theta = -math.pi/2 * r
        self.motion_service.moveTo(x, y, theta) #blocking function

    def turn(self, r):
        if self.stop_request:
            return
        print 'turn',r
        #Turn r deg
        vx = 0.0
        vy = 0.0
        vth = r * math.pi / 180 
        self.motion_service.moveTo(vx, vy, vth) #blocking function

    def setSpeed(self,vx,vy,vth,tm,stopOnEnd=False):
        if self.stop_request:
            return
        self.motion_service.move(vx, vy, vth)
        time.sleep(tm)
        if stopOnEnd:
            self.motion_service.move(0, 0, 0)
            self.motion_service.stopMove()


    # Head motion

    def headPose(self, yaw, pitch, tm):
        jointNames = ["HeadYaw", "HeadPitch"]
        initAngles = [yaw, pitch]
        timeLists  = [tm, tm]
        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, initAngles, timeLists, isAbsolute)


    def headscan(self):
        jointNames = ["HeadYaw", "HeadPitch"]
        # look left
        initAngles = [1.6, -0.2]
        timeLists  = [5.0, 5.0]
        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, initAngles, timeLists, isAbsolute)
        # look right
        finalAngles = [-1.6, -0.2]
        timeLists  = [10.0, 10.0]
        self.motion_service.angleInterpolation(jointNames, finalAngles, timeLists, isAbsolute)
        # look ahead center
        finalAngles = [0.0, -0.2]
        timeLists  = [5.0, 5.0]
        self.motion_service.angleInterpolation(jointNames, finalAngles, timeLists, isAbsolute)
        

    # Arms stiffness [0,1]
    def setArmsStiffness(self, stiff_arms):
        names = "LArm"
        stiffnessLists = stiff_arms
        timeLists = 1.0
        self.motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)
        names = "RArm"
        self.motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)


    # Wait

    def wait(self, r=1):
        print 'wait',r
        for i in range(0,r):
            time.sleep(3)

    # Sensors

    def sensorvalue(self, sensorname='all'):
        if (sensorname == 'frontsonar'):
            return self.sonar[0]
        elif (sensorname == 'rearsonar'):
            return self.sonar[1]
        elif (sensorname == 'headtouch'):
            return self.headTouch
        elif (sensorname == 'lefthandtouch'):
            return self.handTouch[0]
        elif (sensorname == 'righthandtouch'):
            return self.handTouch[1]
        elif (sensorname == 'frontlaser'):
            return self.frontlaser
        elif (sensorname == 'all'):
            return [self.frontlaser,  self.sonar[0],  self.sonar[1],
                self.headTouch, self.handTouch[0], self.handTouch[1] ]


    def sensorvaluestring(self):
        return '%.1f,%.1f,%.1f,%d,%d,%d' %(self.sensorvalue('frontlaser'),self.sensorvalue('frontsonar'),self.sensorvalue('rearsonar'),self.sensorvalue('headtouch'),self.sensorvalue('lefthandtouch'),self.sensorvalue('righthandtouch'))



    # Behaviors

    def normalPosture(self):
        jointValues = [0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01,
                       0, 0, 0, 0, 0]
        isAbsolute = True
        self.motion_service.angleInterpolation(self.jointNames, jointValues, 3.0, isAbsolute)


    def setPosture(self, jointValues):
        isAbsolute = True
        self.motion_service.angleInterpolation(self.jointNames, jointValues, 3.0, isAbsolute)

    def getPosture(self):
        pose = None
        useSensors = True
        pose = self.motion_service.getAngles(self.jointNames, useSensors)
        return pose



    def raiseArm(self, which='R'): # or 'R'/'L' for right/left arm
        if (which=='R'):
            jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            jointValues = [ -1.0, -0.3, 1.22, 0.52, -1.08]
        else:
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
            jointValues = [ -1.0, 0.3, -1.22, -0.52, 1.08]

        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, jointValues, 3.0, isAbsolute)
    
    def lowerArm(self, which='R'):  # or 'L' for left arm
        if (which == 'R'):
            jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            jointValues = [1.5, -0.1, 1.0, 0.3, 0.0]  # relaxed, lowered pose
        else:
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
            jointValues = [1.5, 0.1, -1.0, -0.3, 0.0]

        isAbsolute = True
        self.motion_service.angleInterpolation(jointNames, jointValues, 2.0, isAbsolute)
    
    def greet_user(self):
        self.raiseArm('R')
        time.sleep(1)
        self.lowerArm('R')
    



    def stand(self):
        if self.al_service.getState()!='disabled':
            self.al_service.setState('disabled')
        self.rp_service.goToPosture("Stand",2.0)

    def disabled(self):
        #self.tts_service.say("Bye bye")
        self.al_service.setState('disabled')

    def interactive(self):
        #tts_service.say("Interactive")
        self.al_service.setState('interactive')


    def run_behavior(self, bname):
        if self.beh_service!=None:
            try:
                self.beh_service.startBehavior(bname)
                #time.sleep(10)
                #self.beh_service.stopBehavior(bname)
            except:
                pass

    def sax(self):
        str = 'sax'
        print(str)
        bname = 'saxophone-0635af/behavior_1'
        self.run_behavior(bname)

    def dance(self):
        str = 'dance'
        print(str)
        bname = 'dance/behavior_1'
        self.run_behavior(bname)

    def takephoto(self):
        str = 'take photo'
        print(str)
        #tts_service.say("Cheers")
        bname = 'takepicture-61492b/behavior_1'
        self.run_behavior(bname)

    def introduction(self):
        str = 'introduction'
        print(str)
        bname = 'animated-say-5b866d/behavior_1'
        self.run_behavior(bname)


    # People

    def getPeopleInfo(self):
        pl = self.memory_service.getData('PeoplePerception/PeopleList')
            # PeoplePerception/PeopleList
        print('People list: %s' %str(pl))
        r = []
        for id in pl:
            print('Person ID %d' %id)
            gekey = 'PeoplePerception/Person/%d/GenderProperties' %id
            smkey = 'PeoplePerception/Person/%d/SmileProperties' %id
            agkey = 'PeoplePerception/Person/%d/AgeProperties' %id

            ge = self.memory_service.getData(gekey)  # 0 female, 1 male, confidence
            sm = self.memory_service.getData(smkey)  # 0-1 smile, confidence
            ag = self.memory_service.getData(agkey)  # age, confidence
            d = {}
            d['gender'] = ge
            d['age'] = ag
            d['smile'] = sm
            r.append(d) 
            #rstr= "gender: %s, age: %s, smile: %s" %(str(ge),str(ag),str(sm))
            #print(rtrs)
        return r

    # Battery

    def getBatteryCharge(self):
        return self.battery_service.getBatteryCharge()


    # Memory

    def memset(self, key, val):
        self.memory_service.insertData(key,val)

    def memget(self, key):
        try:
            return self.memory_service.getData(key)
        except:
            return ''

    # Logging functions

    def logenable(self,enable=True):
        if enable:
            if (self.logfile is None):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                logfilename = '/tmp/pepper_%s.log' %timestamp
                self.logfile = open(logfilename,'a')
                self.lthr = threading.Thread(target = self.logthread)
                self.lthr.start()
                print('Log enabled on file %s.' %logfilename)
        else:
            if (self.logfile is not None):
                self.logclose()
                self.lthr.do_run = False
                self.lthr = None
                print('Log disabled.')


    def logdata(self, data):
        if (self.logfile is not None):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.logfile.write("%s;%r\n" %(timestamp, data))
            self.logfile.flush()

    def logclose(self):
        if (self.logfile != None):
            self.logfile.close()
            self.logfile = None


    def logthread(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            try:
                z = self.getState()
                self.logdata(z)
            except:
                pass
            time.sleep(1)


    def setFERserver(self,ip,port=5678):
        self.FER_server_IP = ip
        self.FER_server_port = port


    def getState(self):
        # v1
        # frontlaser, frontsonar, backsonar, headtouch, lefthandtouch, 
        # righthandtouch, screenx, screeny, face, happy
        # v2
        # frontlaser, frontsonar, backsonar, headtouch, lefthandtouch, 
        # righthandtouch, head_yaw, head_pitch, screenx, screeny, touchcnt, face, happy
        
        z = self.sensorvalue() # frontlaser...handtouch
        useSensors = True
        headPose = self.motion_service.getAngles(["HeadYaw", "HeadPitch"],
                                                 useSensors)
        z.append(headPose[0])
        z.append(headPose[1])
        z.append(self.screenTouch[0])
        z.append(self.screenTouch[1])
        z.append(touchcnt)
        z.append(1.0 if self.got_face else 0.0)
        if self.FER_server_IP is not None:
            r = self.sendImage(self.FER_server_IP,self.FER_server_port)
        else:
            r = None
        v = []
        if r is not None and type(r)!=type('str'):
            v = eval(r)
        h = 0.0
        for c in v:
            h = max(h,c[1])
        z.append(h)    
        return z

