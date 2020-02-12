# CircuitPython_MLX90640_DisplayIO

Enhanced version of thermal camera example with PyGamer and MLX90640

I wrote mlx90640_pygamer.py based on mlx90640_simpletest.py from https://github.com/adafruit/Adafruit_CircuitPython_MLX90640
And the example code is advertised on this learn guide from @adafruit: https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera/circuitpython-thermal-camera

The various version here are derived from this original version.

mlx90640_scale.py should work on various size of DisplayIO screen.
This should be used with the right scaling for screen.

Working values of scale_factor start at 3, below this value the text overlap.
For CLUE, the recommended scale is 6.
For PyGamer, the recommended scale is 4.
For PyPortal, the maximum scale is 9.
For PyPortal Titano, the optimal sclae is untested.

It does require at minimum the following library:
* adafruit_bus_device
* adafruit_display_text
* adafruit_fancyled
* adafruit_mlx90640.mpy
* simpleio.mpy

The following version might disapear in the future:
* PyPortal: mlx90640_pyportal.py
* PyGamer: mlx90640_pygamer_plus.py
* CLUE: mlx90640_clue.py

For interactive version, the input need to be adapted to the control or touch scscreen of each board. So those require additional changea and not only the scale_factor.

Feature to be able to save the image will only be implemented on PyGamer and PyPortal as other do not have and SD card build in.

Improvement already implemented:
* Compute and display the average temperature of the center of the sensor
* Indicate the lowest pixel with an O
* Indicate the highest pixel with an X
* Use existing FancyLED library rather than the gradiant code
* PyPortal version that accomodate the bigger screen

Possible improvement not implemented yet:
* Use the button and joystic from the PyGamer
* Use the touch screen of PyPortal
* Use button of CLUE
... to provide a user interface and a few feature:
   * freeze / unfreeze the screen
   * enable / disable 
   * switch between auto-scale and manual scale with lowest/highest temperature
   * compute/display average temperature
   * generate a temperature histogram rather that image

For PyGamer and PyPortal that have an SD card reader:
   * save the image on an SD card ( https://learn.adafruit.com/saving-bitmap-screenshots-in-circuitpython )

For PyPortal or PyGamer with AirLift Feather wing:
   * try sending image over wifi (I don't know how to do that)

For Clue:
   * try sending image over BLE (to what device?)

---

Because I have issues with taking a screen capture, I did not add the SD function.

mlx90640_pygamer_plus+sd.py now record the 32*24 bitmap after 30 frames and the full screen after 60 frames.
This produce the picture.bmp and screen.bmp.

I believe there is a bug in save_pixels from adafruit_bitmapsaver as the screen.bmp does not match what I see on the screen:
1) The last column of pixel from the picture are duplicated to the edge.
2) The three temperature (min, center, max) are not text but colour blob.

Created a 'fake_mlx90640_pygamer+sd.py' that expose the bug on a PyGamer, without the need of a mlx90640. And this produce the picture2.bmp and screen2.bmp.

