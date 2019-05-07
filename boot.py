# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# - - - NETWORKING - - - 
import network
sta_if = network.WLAN(network.STA_IF)

def connectWifi():
  sta_if.active(True)

  # PSID and password for wifi
  sta_if.connect('', '')
  return sta_if
def disconnectWifi():
  sta_if.active(False)

if not sta_if.isconnected():
  print('connecting to network...')
  connectWifi()
  while not sta_if.isconnected():
    pass
print('network config:', sta_if.ifconfig())