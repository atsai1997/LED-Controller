import sys
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, Response
import threading
import netifaces as ni

ni.ifaddresses('wlan0')
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

class Settings:
	def __init__(self):
		self.red_intensity = 0
		self.blue_intensity = 0
		self.green_intensity = 0
		self.state = 0
		self.static = 0

setting = Settings()

app = Flask(__name__)

RED = 13
GREEN = 6
BLUE = 5

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

pr = GPIO.PWM(RED, 50)
pb = GPIO.PWM(BLUE, 50)
pg = GPIO.PWM(GREEN, 50)


@app.route('/postmethod', methods = ['POST'])
def get_post():
	setting.red_intensity = int(request.form['redSlider_data'])
	print(setting.red_intensity)
	setting.blue_intensity = int(request.form['blueSlider_data'])
	print(setting.blue_intensity)
	setting.green_intensity = int(request.form['greenSlider_data'])
	print(setting.green_intensity)
	setting.state = int(request.form['state'])
	print(setting.state)
	setting.static = int(request.form['static'])
	print(setting.static)
	return("OK")

@app.route('/')
def index():
	return render_template('index.html')

def run_app():
	app.run(host=ip, port = 9999, debug = False)

if __name__ == '__main__':
	flask = threading.Thread(name='flask', target=run_app)
	flask.start()
	pr.start(0)
	pb.start(0)
	pg.start(0)

	curr_red = 0
	curr_blue = 0
	curr_green = 0

	red_inc = True
	blue_inc = True
	green_inc = True
	print(setting.state)
	while True:
		if setting.state == 1:
			if setting.static == 0:
				if setting.red_intensity != 0:
					if curr_red >= setting.red_intensity:
						red_inc = False
					elif curr_red == 0:
						red_inc = True
					if red_inc:
						curr_red += 1
					else:
						curr_red -= 1
				if setting.blue_intensity != 0:
					if curr_blue >= setting.blue_intensity:
						blue_inc = False
					elif curr_blue == 0:
						blue_inc = True
					if blue_inc:
						curr_blue += 1
					else:
						curr_blue -= 1
				if setting.green_intensity != 0:
					if curr_green >= setting.green_intensity:
						green_inc = False
					elif curr_green == 0:
						green_inc = True
					if green_inc:
						curr_green += 1
					else:
						curr_green -= 1

				pr.ChangeDutyCycle(curr_red)
				pb.ChangeDutyCycle(curr_blue)
				pg.ChangeDutyCycle(curr_green)
	
				sleep(.01)
			else:
				pr.ChangeDutyCycle(setting.red_intensity)
				pb.ChangeDutyCycle(setting.blue_intensity)
				pg.ChangeDutyCycle(setting.green_intensity)
		else:
			pr.ChangeDutyCycle(0)
			pb.ChangeDutyCycle(0)
			pg.ChangeDutyCycle(0)
			curr_red = 0
			curr_blue = 0
			curr_green = 0
