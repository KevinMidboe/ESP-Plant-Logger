First prototype has a ESP8266[0][1] strapped on a soil moisture sensor [2]. The the small form factor, easily flash-able firware and gpio pins made the ESP8266 a great fit for the task. The main focus is the try transmit the soil moisture of a plant to an elasticsearch endpoint. Kibana is used to visialize the time since laste watered compared to the soil moisture.

Using micropython to interface with the pins and it makes it easy to send json data to our elastic endpoint. 
Guide on how to flash your esp8266 with micropython can be found here: . 

Excecution path:
 + boot.py - Start with setting up wifi
 + main.py - Import logger. Call watercontent()
 + watercontent.py
   - Reads analog pin for sensor data
   - logMoisture inputs this value and after getting the ntp time is, sets up a json payload and sends it to logger.
 + elasticLog.py - inputs json payload and sends it to elastic endpoint using urequests.



Measuring the power draw:
 Log interval 10 seconds using sleep
04.05.19
19:47 - 0 mAh
20:09 - 10 mAh
01:34 - 133 mAh
05.05.19
 - 
06.05.19
22:30 - 556mAh

 Log interval 30 seconds using deepsleep[3][4]
22:30 - 0 mAh
00:01 - 5 mAh
07:36 - 30 mAh
16:58 - 65 mAh


TODO:
 - Special characters ÆØÅ seem to not be supported.
 - Wifi and elastic settings should be in a config
 - [Research] Get a better understanding of how our code executes
 - Add light and temperature sensors. Extend analog pins available with 4051 multiplexer.  



Notes:
	Deepsleep
If the code execution takes 100ms right before entering deepsleep there will be no time to connect and upload any new files to the chip. Remember to either have a your program check if a known digital pin is set to high which can act as a cutoff of main program execution by placing a jumper between power* and the known pin. Another way to allow a way of still interfacing with the board is by using machine.Timer[5][6] to create a callback to main function, all while giving us a window to interface or stop execution, delayed by a set interval e.g. 3 seconds. 
* Double check that this should not be to ground pin.

	Wemos D1 ESP8266 Pin for deepsleep
While most documentation says to connect RESET/RST to pin D8 (physical ping 16), this does not apply to this board. Instead us pin D0 (physical pin 4)!

[0] WTF is ESP8266
[1] Image of the chip
[2] And image of soil stick
[3] Deep sleep docs
[4] Our implementation of deepsleep
[5] docs
[4] Our implementation of machine.Timer