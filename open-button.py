import RPi.GPIO as GPIO
import httplib, time, sys

from yopy import Yo

from secret import YO_API_KEY

TIMEOUT = 0.1 #seconds
API_HOST = "hackerspace.idi.ntnu.no"
API_ENDPOINT = "/api/door/push"
GPIO_PIN = 15 

YO = Yo(YO_API_KEY)


def check_button(state):
  # Read state from GPIO.
  gpio = GPIO.input(GPIO_PIN)

  if state != gpio:
    # State has changed, create connection to API.
    conn = httplib.HTTPConnection(API_HOST)

    if gpio == 1:
      conn.request('POST', API_ENDPOINT)
      print "Button pressed. Sent door open signal"

      try:
        YO.yoall()
        print "Yo!"
      except:
        print "Yo API error:"
        print sys.exc_info()[0]
    else:
      print "Button released."
  return gpio


if __name__ == '__main__':
  # Initialize the GPIO.
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

  # Initialize state to 0.
  state = 0

  try:
      print "Connected to api.justyo.co. {} people are subscribed!".format(YO.number())
  except KeyError:
      print "Error connecting to api.justyo.co. Did you remember to put YO_API_KEY in secret.py?"
      exit(1)

  while True:
    # Sleep between checks, and run forever.
    state = check_button(state)
    time.sleep(TIMEOUT)
