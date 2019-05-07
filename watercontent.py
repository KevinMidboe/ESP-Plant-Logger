import ntptime
from time import sleep
from machine import ADC, deepsleep, DEEPSLEEP, RTC, Timer
from boot import connectWifi, disconnectWifi
from elasticLog import logger

signalPin = ADC(0)
NTP_OFFSET = 946684800
DEEPSLEEP_TIME=30   # in seconds

def logMoisture(reading):
  try:
    time = ntptime.time()
    time = time + NTP_OFFSET

    data = {
      '@timestamp': int(time*1000),
      'moisture': reading,
      'message': 'Moisture reading',
      'plant_id': 2,
      'plant_name': 'Gulrorbambus'
    }
    return logger('Moisture reading', data=data)
  except OSError as e:
    logger('Error', data={'message': 'Error fetching ntp time', 'error': e})


def watercontent():
  moistureReading = signalPin.read()

  print(logMoisture(moistureReading))
  # A little extra time alive for file transfere
  print('3 second upload window before deepsleep')
  sleepTriggerTimer = Timer(-1)
  sleepTriggerTimer.init(period=3000, mode=Timer.ONE_SHOT, callback=_sleep)

def _sleep(_):
  print('deepsleep starting for {} seconds'.format(DEEPSLEEP_TIME))
  rtc = RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
  rtc.alarm(rtc.ALARM0, DEEPSLEEP_TIME * 1000)
  deepsleep()