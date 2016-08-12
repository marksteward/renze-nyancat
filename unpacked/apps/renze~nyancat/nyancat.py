### Category: Other
### Author: Rosa Luxus
### License: MIT
### Appname: Nyancat
### Description: Nyancat. Animated. Infinite.

import buttons
import ugfx
import pyb
from imu import IMU

ugfx.init()
ugfx.clear()
ugfx.orientation(180)
orientation = ugfx.orientation()
imu=IMU()
buttons.init()
ugfx.set_default_font(ugfx.FONT_NAME)

while True:
	for i in range(1,11):
		ugfx.display_image(0, 0, "apps/renze~nyancat/nyan_%d.gif" % i)
		if buttons.is_triggered("BTN_MENU") or buttons.is_triggered("BTN_B") or buttons.is_triggered("JOY_CENTER"):
			break
		ival = imu.get_acceleration()
		if ival['y'] < -0.5:
			if orientation != 0:
				ugfx.orientation(0)
		elif ival['y'] > 0.5:
			if orientation != 180:
				ugfx.orientation(180)
		if orientation != ugfx.orientation():
			orientation = ugfx.orientation()

ugfx.clear()