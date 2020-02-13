### mlx90640_scale_pygamer.py

import time
import board
import busio
import adafruit_mlx90640
import displayio
import terminalio
from adafruit_display_text.label import Label
from simpleio import map_range
import adafruit_fancyled.adafruit_fancyled as fancy

# On PyPortal, the scale factor works from 3 to 9
scale_factor = 4
text_x = (32 * scale_factor) - 30
text_y = (24 * scale_factor) + 8

gradian_y = 24 + int (20 / scale_factor)

#gradian_y = int( (text_y + 8) / 2 )

number_of_colors = 32                          # Number of color in the gradian
last_color = number_of_colors-1                # Last color in palette
palette = displayio.Palette(number_of_colors)  # Palette with all our colors

# gradian for fancyled palette generation
grad = [(0.00, fancy.CRGB(0, 0, 255)),    # Blue
        (0.25, fancy.CRGB(0, 255, 255)),
        (0.50, fancy.CRGB(0, 255, 0)),    # Green
        (0.75, fancy.CRGB(255, 255, 0)),
        (1.00, fancy.CRGB(255, 0, 0))]    # Red

# create our palette using fancyled expansion of our gradian
fancy_palette = fancy.expand_gradient(grad, number_of_colors)
for c in range(number_of_colors):
    palette[c] = fancy_palette[c].pack()

# Bitmap for colour coded thermal value
image_bitmap = displayio.Bitmap( 32, 24, number_of_colors )
# Create a TileGrid using the Bitmap and Palette
image_tile= displayio.TileGrid(image_bitmap, pixel_shader=palette)
# Create a Group that scale 32*24 to 256*192
image_group = displayio.Group(scale=scale_factor)
image_group.append(image_tile)

scale_bitmap = displayio.Bitmap( number_of_colors, 1, number_of_colors )

# Create a Group Scale
scale_group = displayio.Group(scale=scale_factor)
scale_tile = displayio.TileGrid(scale_bitmap, pixel_shader=palette, x = 0, y = gradian_y)
scale_group.append(scale_tile)

for i in range(number_of_colors):
    scale_bitmap[i, 0] = i            # Fill the scale with the palette gradian

# Create the super Group
group = displayio.Group(max_size = 8)

min_label = Label(terminalio.FONT, max_glyphs=10, color=palette[0], x=0, y=text_y)
center_label = Label(terminalio.FONT, max_glyphs=10, color=palette[int(number_of_colors/2)], x=int (text_x/2), y=text_y)
max_label = Label(terminalio.FONT, max_glyphs=10, color=palette[last_color], x=text_x, y=text_y)

# Indicator for the minimum and maximum location
o_label = Label(terminalio.FONT, max_glyphs = 1, text = "o", color = 0xFFFFFF, x = 0, y = 0)
x_label = Label(terminalio.FONT, max_glyphs = 1, text = "x", color = 0xFFFFFF, x = 0, y = 0)

# Add all the sub-group to the SuperGroup
group.append(image_group)
group.append(scale_group)
group.append(min_label)
group.append(center_label)
group.append(max_label)
group.append(o_label)
group.append(x_label)

# Add the SuperGroup to the Display
board.DISPLAY.show(group)

min_t = 20       # Initial minimum temperature range, before auto scale
max_t = 37       # Initial maximum temperature range, before auto scale

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")

#mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

frame = [0] * 768

while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:           # these happen, no biggie - retry
        continue

#    print("Time for data aquisition: %0.2f s" % (time.monotonic()-stamp))

    mini = frame[0]       # Define a min temperature of current image
    maxi = frame[0]       # Define a max temperature of current image

    minx = 0
    miny = 0
    maxx = 23
    maxy = 31

    for h in range(24):
        for w in range(32):
            t = frame[h*32 + w]
            if t < mini:
                mini = t
                minx = w
                miny = h
            if t > maxi:
                maxi = t
                maxx = w
                maxy = h
            image_bitmap[w, (23-h)] = int(map_range(t, min_t, max_t, 0, last_color ))

    # min and max temperature indicator
    min_label.text="%0.2f" % (min_t)
    max_label.text="%0.2f" % (max_t)
#    max_string="%0.2f" % (max_t)
#    max_label.x=248-(5*len(max_string))      # Tricky calculation to left align
#    max_label.text=max_string

    # Compute average_center temperature of the middle of sensor and convert to palette color
    center_average = (frame[11*32 + 15] + frame[12*32 + 15] + frame[11*32 + 16] + frame[12*32 + 16]) / 4
    center_color = int(map_range(center_average, min_t, max_t, 0, last_color ))
    center_label.text = "%0.2f" % (center_average)
    center_label.color = palette[center_color]

    # Set the location of X for lowest temperature
    x_label.x = maxx * scale_factor
    x_label.y = (23-maxy) * scale_factor

    # Set the location of O for highest temperature
    o_label.x = minx * scale_factor
    o_label.y = (23-miny) * scale_factor

    min_t = mini                  # Automatically change the color scale
    max_t = maxi

#    print((mini, maxi))           # Use this line to display min and max graph in Mu
#    print("Total time for aquisition and display %0.2f s" % (time.monotonic()-stamp))
