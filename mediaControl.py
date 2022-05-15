import os
import serial
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from serial.tools import list_ports

#  This will get the audio device and its parameters for the computer
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the current volume and range for the computer
current_vol = volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()

pyautogui.FAILSAFE = False

# Saves the first row from range
currentRange = volumeRange[0]

# This function checks which COM-port my Arduino is using so that it can communicate with this python script
def find_port():
    all_port_tuples = list_ports.comports()
    for ap, _, _ in all_port_tuples:
        port = os.path.basename(ap)
        if port == 'COM3' or port == 'COM5':
            return port

port = find_port()

# Connecting to the Arduino serial port
board = serial.Serial(port, 9600)

# The program starts here. This function is responsible for the adjustments of the volume.
# Media can be paused and played by single-pressing the button.
# Also the volume will be muted when double pressing the button.
def mode1():
    while True:
        response = board.readline().decode("latin-1").strip()
        if response == "mode2":
            mode2()
        elif response == "pause" or response == "play":
            pyautogui.press("playpause")
        elif response == "mute":
            pyautogui.press("volumemute")
        else:
            if currentRange == -70:
                volume.SetMasterVolumeLevel(vol_calibration2(int(response)), None)
            else:
                volume.SetMasterVolumeLevel(vol_calibration1(int(response)), None)

# If you hold the button for 1 second the program will switch into what I call "shuffle mode" or mode 2.
# This will let you switch between songs by rotating the rotary encoder clockwise or anti-clockwise.
# Media can still be paused, played and muted in this mode.
def mode2():
    while True:
        response = board.readline().decode("latin-1").strip()
        if response == "mode1":
            mode1()
        elif response == "pause" or response == "play":
            pyautogui.press("playpause")
        elif response == "mute":
            pyautogui.press("volumemute")
        else:
            if(response == "nexttrack"):
                pyautogui.press("nexttrack")
            if(response == "prevtrack"):
                pyautogui.press("prevtrack")


# The module that is used to change the volume of the computer is called Pycaw.
# The range in which the volume is inbetween does not correspond with the computer 0-100.
# In order to obtain that, I had to create an array and save the corresponding volume level to that particular value in the range.
# I've noticed that sometimes the range changes, so I've created two sets of array that correspond to each range.

# This will be used if range is (-65.25, 0.0)
def vol_calibration1(x):
    cal = {
            0: -65.25, 1: -56.99, 2: -51.67, 3: -47.74, 4: -44.62, 5: -42.03, 6: -39.82, 7: -37.89, 8: -36.17,9: -34.63,
            10: -33.24, 11: -31.96, 12: -30.78, 13: -29.68, 14: -28.66, 15: -27.7, 16: -26.8, 17: -25.95, 18: -25.15, 19: -24.38,
            20: -23.65, 21: -22.96, 22: -22.3, 23: -21.66, 24: -21.05, 25: -20.46, 26: -19.9, 27: -19.35, 28: -18.82, 29: -18.32,
            30: -17.82, 31: -17.35, 32: -16.88, 33: -16.44, 34: -16.0, 35: -15.58, 36: -15.16, 37: -14.76, 38: -14.37, 39: -13.99,
            40: -13.62, 41: -13.26, 42: -12.9, 43: -12.56, 44: -12.22, 45: -11.89, 46: -11.56, 47: -11.24, 48: -10.93, 49: -10.63,
            50: -10.33, 51: -10.04, 52: -9.75, 53: -9.47, 54: -9.19, 55: -8.92, 56: -8.65, 57: -8.39, 58: -8.13, 59: -7.88,
            60: -7.63, 61: -7.38, 62: -7.14, 63: -6.9, 64: -6.67, 65: -6.44, 66: -6.21, 67: -5.99, 68: -5.76, 69: -5.55,
            70: -5.33, 71: -5.12, 72: -4.91, 73: -4.71, 74: -4.5, 75: -4.3, 76: -4.11, 77: -3.91, 78: -3.72, 79: -3.53,
            80: -3.34, 81: -3.15, 82: -2.97, 83: -2.79, 84: -2.61, 85: -2.43, 86: -2.26, 87: -2.09, 88: -1.91, 89: -1.75,
            90: -1.58, 91: -1.41, 92: -1.25, 93: -1.09, 94: -0.93, 95: -0.77, 96: -0.61, 97: -0.46, 98: -0.3, 99: -0.15, 100: 0.0
          }
    return cal[x]

# This will be used if range is (-70.0, 5.0)
def vol_calibration2(x):
    cal = {
            0: -70, 1: -57.54, 2: -50.78, 3: -46.12, 4: -42.56, 5: -39.68, 6: -37.25, 7: -35.17, 8: -33.33, 9: -31.69,
            10: -30.21, 11: -28.86, 12: -27.63, 13: -26.48, 14: -25.42, 15: -24.42, 16: -23.49, 17: -22.61, 18: -21.77, 19: -20.99,
            20: -20.24, 21: -19.53, 22: -18.84, 23: -18.19, 24: -17.57, 25: -16.96, 26: -16.39, 27: -15.83, 28: -15.29, 29: -14.77,
            30: -14.27, 31: -13.78, 32: -13.31, 33: -12.86, 34: -12.41, 35: -11.98, 36: -11.56, 37: -11.16, 38: -10.76, 39: -10.37,
            40: -9.99, 41: -9.63, 42: -9.27, 43: -8.92, 44: -8.57, 45: -8.24, 46: -7.91, 47: -4.70, 48: -7.27, 49: -6.96,
            50: -6.66, 51: -6.37, 52: -6.07, 53: -5.79, 54: -5.51, 55: -5.23, 56: -4.96, 57: -8.39, 58: -4.44, 59: -4.18,
            60: -3.93, 61: -3.68, 62: -3.44, 63: -3.20, 64: -2.96, 65: -2.73, 66: -2.50, 67: -2.27, 68: -2.05, 69: -1.83,
            70: -1.61, 71: -1.40, 72: -1.19, 73: -0.98, 74: -0.78, 75: -0.58, 76: -0.38, 77: -0.18, 78: -0.01, 79: -0.21,
            80: 0.40, 81: 0.6, 82: 0.81, 83: 1.01, 84: 1.22, 85: 1.43, 86: 1.64, 87: 1.86, 88: 2.08, 89: 2.30,
            90: 2.53, 91: 2.76, 92: 2.99, 93: 3.23, 94: 3.47, 95: 3.71, 96: 3.96, 97: 4.22, 98: 4.47, 99: 4.73, 100: 5.0
         }
    return cal[x]

# Triggering the program
mode1()