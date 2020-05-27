# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC orginazers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ========================================================================
# SCRIPT USED FOR WIRING ALL COMPONENTS
# ========================================================================
import sys

sys.path.append('.')

import time
import signal  # 信号处理函数， Linux上使用完整，预设信号处理函数，暂停并等待信号，以及定时发出SIGALRM等
from multiprocessing import Pipe, Process, Event  # 多过程库中

# hardware imports
from src.hardware.camera.cameraprocess import CameraProcess
from src.hardware.serialhandler.serialhandler import SerialHandler

# data imports
# from src.data.consumer.consumerprocess             import Consumer

# utility imports
from src.utils.camerastreamer.camerastreamer import CameraStreamer
from src.utils.cameraspoofer.cameraspooferprocess import CameraSpooferProcess
from src.utils.remotecontrol.remotecontrolreceiver import RemoteControlReceiver

from src.dataacquisition.lanedetectionprocess import LaneDetectionProcess
from src.dataacquisition.sensordatahandler import SensorDataHandler
from src.dataacquisition.objectdetectionprocess import ObjectDetectionProcess
from src.utils.debugger.initlogger import InitLogger

# =============================== CONFIG =================================================
enableStream = True
enableCameraSpoof = True
enableRc = False
enableExec = True
# ================================ PIPES ==================================================


# gpsBrR, gpsBrS = Pipe(duplex = False)           # gps     ->  brain
# ================================ PROCESSES ==============================================
allProcesses = list()

# =============================== HARDWARE PROCC =========================================
# ------------------- camera + streamer ----------------------
if enableStream:
    camStR, camStS = Pipe(duplex=False)  # camera  ->  streamer

    if enableCameraSpoof:
        camSpoofer = CameraSpooferProcess([], [camStS], '001',".h264")
        allProcesses.append(camSpoofer)

    else:
        camProc = CameraProcess([], [camStS])
        allProcesses.append(camProc)

    streamProc = CameraStreamer([camStR], [])
    allProcesses.append(streamProc)

# =============================== DATA ===================================================
# gps client process
# gpsProc = GpsProcess([], [gpsBrS])
# allProcesses.append(gpsProc)

if enableExec:
    # before to create all the interconnection and the process
    # initialize the logger object
    init_logger = InitLogger()
    print("i am here")
    camStR,camStS = Pipe(duplex=False)   #camera - streamer
    # create a connection between the camera and the Lane Detector
    cameraStrR, cameraStrS = Pipe(duplex=False)
    # create a connection between the camera handler and the Object Detector
    cameraStr2R, cameraStr2S = Pipe(duplex=False)
    # create a connection between the serial handler and the Lane Detector
    commandR, commandS = Pipe(duplex=False)
    # create a connection between the serial handler and the Object Detector
    command2R, command2S = Pipe(duplex=False)
    # create a connection between the serial handler and the Sensor Data Acquirer
    msrAcqR, msrAcqS = Pipe(duplex=False)

    #cameraProc = CameraProcess([], [cameraStrS, cameraStr2S])
    #allProcesses.append(cameraProc)

    camSpoofer = CameraSpooferProcess([], [camStS], 'training',".h264")
    #laneDetecProc = LaneDetectionProcess([cameraStrR], [commandS])
    #allProcesses.append(laneDetecProc)

    objectDetecProc = ObjectDetectionProcess([cameraStr2R], [command2S])
    allProcesses.append(objectDetecProc)

    #serialhandler = SerialHandler([commandR, command2R], [msrAcqS])
    # allProcesses.append(serialhandler)

    dataHandler = SensorDataHandler([msrAcqR], [])
    allProcesses.append(dataHandler)

# ===================================== CONTROL ==========================================
# ------------------- remote controller -----------------------
if enableRc:
    rcShR, rcShS = Pipe(duplex=False)  # rc      ->  serial handler

    # serial handler process
    shProc = SerialHandler([rcShR], [])
    allProcesses.append(shProc)

    rcProc = RemoteControlReceiver([], [rcShS])
    allProcesses.append(rcProc)

print("Starting the processes!", allProcesses)
for proc in allProcesses:
    proc.daemon = True
    proc.start()

blocker = Event()

try:
    blocker.wait()
except KeyboardInterrupt:
    print("\nCatching a KeyboardInterruption exception! Shutdown all processes.\n")
    for proc in allProcesses:
        if hasattr(proc, 'stop') and callable(getattr(proc, 'stop')):
            print("Process with stop", proc)
            proc.stop()
            proc.join()
        else:
            print("Process witouth stop", proc)
            proc.terminate()
            proc.join()
