# Setup

I have used a Wemos D1 with ESP8266, the following will (per now) only describe setup with this chip, your mileage may vary.  
 - Find the chip over a serial connection
 - Flashing micropython
 - Transfere files to chip
 - Add sensors
 - (Elasticsearch)
 - (Kibana dashboards)

## Find the chip over a serial connection
The Wemos D1 uses a ch341 chip to convert our serial chip output to usb protocol. To get started download the CH341 chip driver here https://sparks.gogo.co.nz/ch340.html, or find another site with the driver.  
After installed and rebooted the mac the chip should appear at "/dev/tty\*" after plugging the micro usb into your usb. As an example the output of `/dev/` shows me the following:  
```bash
user@host: ls /dev/tty.*

...
```

In my case the `/dev/tty.usbmodem1420` is the interface we want to connect to. Now we could connect directly to the chips serial connection we first want to flash the chip with microPython.

 - download link for microPython
 - ampy download
 - ampy commands
  - getting info
 - ampy flash
We will get back to transfering files with ampy in the next section.


Connecting to the serial interface:
This for me is the coolest part of builds like this. Connecting and interfacing with a chip over a interface communly used since the mid-80s. The easiest I found was to use `screen`. If your not familiar a quick guide can be found here: []. Screen is a full-screen window manager that multiplexes a physical terminal between several processes (typically interactive shells). Each virtual terminal provides the functions of your normal terminal. This enables us to open a virtual terminal that displays what our microcontrollers prompt over the serial connection. 

```bash
screen /dev/tty.usbmodem1420 9600
```
 - - - 
The number at the end is the baud rate (it's a measure of symbol rate and is one of the components that determine the speed of communication over a data channel).


### Transfering files to the chip
We use ampy again with the following command: ` `

## Some important behaviour:
 - boot.py is called where we can setup e.g. sensors, pins and wifi.
 - main.py is always called after boot is finished, this will most oftenly be the execution start of our program. 
(More details can be found here)

## Tricks: 
 - os.listdir()
 - machine.Timer use for timeouts without normal time package.
 - ntptime to get universal time. Also our offset

### ntptime for universal time
We don't have a OS that handles setting the correct time based on the location. What we could use instead is the ntp protocol to fetch a time. Network Time Protocol (NTP) has been in operation since before 1985, and is one of the oldest Internet protocols in current use. This means it's most likely even going to be included in microPython. 

 I needed to calculate a different offset to translate the ntp time to epoch (time since 1970). The offset I used was 946684800. Add this to your ntp time. E.g:

 ```python
 NTP_OFFSET = 946684800
 ntpTime = ntptime.time()
 epochTime = ntpTime + NTP_OFFSET
 ```

 - - -
# Notes
First prototype has a ESP8266[0][1] strapped on a soil moisture sensor [2]. The the small form factor, easily flash-able firware and gpio pins made the ESP8266 a great fit for the task. The main focus is the try transmit the soil moisture of a plant to an elasticsearch endpoint. Kibana is used to visialize the time since laste watered compared to the soil moisture.

Using micropython to interface with the pins and it makes it easy to send json data to our elastic endpoint. 
Guide on how to flash your esp8266 with micropython can be found here: . 

## Excecution path:
 + boot.py - Start with setting up wifi
 + main.py - Import logger. Call watercontent()
 + watercontent.py
   - Reads analog pin for sensor data
   - logMoisture inputs this value and after getting the ntp time is, sets up a json payload and sends it to logger.
 + elasticLog.py - inputs json payload and sends it to elastic endpoint using urequests.  

## Measuring the power draw:  
### Log interval 10 seconds using sleep  
04.05.19  
19:47 - 0 mAh  
20:09 - 10 mAh  
01:34 - 133 mAh  
05.05.19
 \-   
06.05.19  
22:30 - 556mAh  
   
### Log interval 30 seconds using deepsleep[3][4]  
22:30 - 0 mAh   
00:01 - 5 mAh  
07:36 - 30 mAh  
16:58 - 65 mAh  
 

## TODO:
 - Special characters ÆØÅ seem to not be supported.
 - Wifi and elastic settings should be in a config
 - [Research] Get a better understanding of how our code executes
 - Add light and temperature sensors. Extend analog pins available with 4051 multiplexer.  



## Meta notes:
### Deepsleep
If the code execution takes 100ms right before entering deepsleep there will be no time to connect and upload any new files to the chip. Remember to either have a your program check if a known digital pin is set to high which can act as a cutoff of main program execution by placing a jumper between power* and the known pin. Another way to allow a way of still interfacing with the board is by using machine.Timer[5][6] to create a callback to main function, all while giving us a window to interface or stop execution, delayed by a set interval e.g. 3 seconds. 
* Double check that this should not be to ground pin.

### Wemos D1 ESP8266 Pin for deepsleep
While most documentation says to connect RESET/RST to pin D8 (physical ping 16), this does not apply to this board. Instead us pin D0 (physical pin 4)!

[0] WTF is ESP8266  
[1] Image of the chip  
[2] And image of soil stick  
[3] Deep sleep docs  
[4] Our implementation of deepsleep  
[5] docs  
[4] Our implementation of machine.Timer  
