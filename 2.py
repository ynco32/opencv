"""

2. A clock having two needles (hour and minute)

   - Can you make the clock synchrozed with your computer clock?


"""

import cv2
import numpy as np 
import datetime
import math

def DIY_getline(x0, y0, x1, y1):
    points = []
    inclination = 0
    if x0 != x1:
        inclination =  (y0-y1) / (x0-x1)
    

    if (inclination > 1) or (inclination < -1):
        if y0 > y1:
            for y in range(y1, y0-1, 1):
                x = (y-y0)*(x1-x0)/(y1-y0) + x0
                print(f"x: {x}, y: {y}")
                xint = int(x)
                points.append((xint, y))
        else:
            for y in range(y0,y1+1):
                if y0 == y1: 
                    x= x0
                else:
                    x = (y-y0)*(x1-x0)/(y1-y0) + x0
                xint = int(x)
                points.append((xint, y))
            
    else:
        if x0 > x1:
            for x in range(x1, x0-1, 1):
                y = (x-x0)*(y1-y0)/(x1-x0) + y0
                yint = int(y)
                points.append((x, yint))

        else:
            for x in range(x0,x1+1):
                if x0 == x1: 
                    y= y0
                else:
                    y = (x-x0)*(y1-y0)/(x1-x0) + y0
                yint = int(y)
                points.append((x, yint))
    return points



def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    xys = DIY_getline(x0, y0, x1, y1)
    
    for xy in xys:
        x, y = xy
        canvas[y, x] = color
    return
#


def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 
#


def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 
#


def get_hr_init():
	hr_init = []
	
	for i in range(0, 360, 6):
		x = int(1000 + 500 * math.cos(i * math.pi / 180))
		y = int(1000 + 500 * math.sin(i * math.pi / 180))

		hr_init.append((x, y))

	return hr_init

def get_hr_dest():
    hr_dest = []
    for i in range(0, 360, 6):
        x = int(1000 + (500-20) * math.cos(i * math.pi / 180))
        y = int(1000 + (500-20) * math.sin(i * math.pi / 180))
        hr_dest.append((x, y))
        
    return hr_dest



def draw_time(canvas):
	time_now = datetime.datetime.now().time()
	hour = math.fmod(time_now.hour, 12)
	minute = time_now.minute
	second = time_now.second

	second_angle = math.fmod(second * 6 + 270, 360)
	minute_angle = math.fmod(minute * 6 + 270, 360)
	hour_angle = math.fmod((hour*30) + (minute/2) + 270, 360)

	x_sec = int(1000 + (500-25) * math.cos(second_angle * math.pi / 180))
	y_sec = int(1000 + (500-25) * math.sin(second_angle * math.pi / 180))
	drawLine(canvas, 1000, 1000, x_sec, y_sec, (255,255,255))

	x_min = int(1000 + (500-60) * math.cos(minute_angle * math.pi / 180))
	y_min = int(1000 + (500-60) * math.sin(minute_angle * math.pi / 180))
	drawLine(canvas, 1000, 1000, x_min, y_min, (255,50,0))

	x_hr = int(1000 + (500-100) * math.cos(hour_angle * math.pi / 180))
	y_hr = int(1000 + (500-100) * math.sin(hour_angle * math.pi / 180))
	drawLine(canvas,1000,1000, x_hr, y_hr, (255,50,0))

	cv2.circle(canvas, (1000,1000), 5, (50, 50, 50), -1)

	return canvas


def main():
    width, height = 2000, 2000
    canvas = np.zeros( (height, width, 3), dtype='uint8')
    
    hr_init = get_hr_init()
    hr_dest = get_hr_dest()
    
    for i in range(len(hr_init)):
        if i % 5 == 0:
            drawLine(canvas, hr_init[i][0], hr_init[i][1], hr_dest[i][0], hr_dest[i][1], (255,255,255))
        else:
            cv2.circle(canvas, hr_init[i], 5, (125,125,125), -1)


    while True:
        image_original = canvas.copy()

        clock_face = draw_time(image_original)

        cv2.imshow('clock', image_original)
        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__": # __ 
    main()