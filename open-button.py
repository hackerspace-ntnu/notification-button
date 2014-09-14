import RPi.GPIO as GPIO
import httplib, time

TIMEOUT = 0.1 #seconds
API_HOST = "hackerspace.idi.ntnu.no"
API_ENDPOINT = "/api/door/push"
GPIO_PIN = 15 

def check_button(state):
  # Read state from GPIO.
  gpio = GPIO.input(GPIO_PIN)

  if state != gpio:
    # State has changed, create connection to API.
    conn = httplib.HTTPConnection(API_HOST)

    if gpio == 1:
      conn.request('POST', API_ENDPOINT)
      print "Button pressed. Sent door open signal"
    else:
      print "Button released."
  return gpio

if __name__ == '__main__':
  # Initialize the GPIO.
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

  # Initialize state to 0.
  state = 0

  while True:
    # Sleep between checks, and run forever.
    state = check_button(state)
    time.sleep(TIMEOUT)
