# MediaKnob

Volume and media controller built using an Arduino Nano and a rotary encoder.

![3D-model](https://github.com/AhmadMD16/MediaKnob/blob/main/images/3D-printed-case-v2.png)

## Description

We will be going through the proccess of building this volume control from start to finish. The reason as to why I've used an Arduino Nano for this build is because it was the only thing I had available at home and I'm too lazy and broke to buy anything else. The downside of this board however is that it does not have support for HID, which means we can't use the HID-Project library from NicoHood. For more info regarding what boards are compatible with HID library and instructions for setting the board up, check NicoHood's github page here:

https://github.com/NicoHood/HID

So you might be wondering, how do we get it to work without the HID support. Well one way to solve this issue is by letting the Arduino communicate with your PC via serial. The python program in this repository picks up the values and other serial inputs from you Arduino and then adjusts the volume/controls your media.

## Getting Started
This volume/media controller does not require a bunch of components which makes it a fun project for those who want to create something small and relatively cheap.

The components used for this build are:

* Arduino Nano
* Rotary Encoder

There is a few steps that needs to be done for this to be working. You will need to connect the components as shown in the following schematic. 

![Schematic](https://github.com/AhmadMD16/MediaKnob/blob/main/images/Circuit.png)

Next step is to install the Arduino file and upload it to your Arduino Nano. Once you've done that you can open up the Serial Monitor in the Arduino IDE and try to rotate the rotary encoder. If everything is hooked up correctly you should see a value changing between 0-100, that's the value for the volume. Last step is to download and run the Python file and install all the required modules. Once that is done you will be good to go. Try to rotate the rotary encoder now and you will see the volume changing. 

You can press the rotary encoder once and it should pause/play music, while double pressing should mute the audio. If you hold down the button for one second you will enter what I call the "Shuffle mode". What it does is that if you want to skip to the next song or the previous, all you need to do is to rotate it either clockwise or counter clockwise. You can then go back to changing the volume by holding the rotary encoder for one second.

### Controls

- click: Play/Pause
- double click: Mute/Un-mute
- rotate: volume up and down
- hold (1000 ms): Enter/Exit Shuffle mode

### Dependencies

This program only works for Windows.

### Help

If you stumble upon any connection problems with the COM-ports, change the code in the find_port() function to the port your Arduino is connected to.
