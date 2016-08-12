import ugfx
import pyb

ugfx.init()
ugfx.clear()
ugfx.orientation(180)

#for i in range(1,2):
#  ugfx.display_image(0, 0, "love%d.gif" % i)
#  pyb.delay(500);
ugfx.display_image(0, 0, "love0.gif")
pyb.delay(10000);