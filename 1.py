
"""
1. Stars Twinkling in the night sky. Improvise.

"""


""" 

1. functions: makeRmat(), makeTmat()  (2 points)

2. draw the pentagon system (2 points)

3. use DIY getline() function (3 points)

4. submit one python code file and a pdf file explaining all the theories, 
math, and methods used in the python code.  (2 points)


"""



import numpy as np 
import cv2 

def DIY_getline(x0, y0, x1, y1):
    points = []
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


def getRegularPentagon():
    delta = 360. / 5
    points = []
    for i in range(5):
        degree = i * delta 
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append( (x, y, 1) )
    #
    points = np.array(points)
    return points
#


def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 
#


def drawStars(canvas, pts, color):
    for k in range(pts.shape[0]-2):
        drawLine(canvas, pts[k,0], pts[k,1], pts[k+2,0], pts[k+2,1], color)
        
    for k in range(pts.shape[0]-3):
        drawLine(canvas, pts[k,0], pts[k,1], pts[k+3,0], pts[k+3,1], color)
                    

    return 


def makeRmat(degree, points):
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)

    #make Rmat
    Rmat = np.zeros((3,3))
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[0,2] = 0
    Rmat[1,0] = s
    Rmat[1,1] = c
    Rmat[1,2] = 0
    Rmat[2,0] = 0
    Rmat[2,1] = 0
    Rmat[2,2] = 1

    #calculate Rmat
    qT = Rmat @ points.T
    points = qT.T 
    return points 


def makeTmat(tx, ty, points):
    #make Tmat
    Tmat = np.zeros((3,3))
    Tmat[0,0] = 1
    Tmat[0,1] = 0
    Tmat[0,2] = tx
    Tmat[1,0] = 0
    Tmat[1,1] = 1
    Tmat[1,2] = ty
    Tmat[2,0] = 0
    Tmat[2,1] = 0
    Tmat[2,2] = 1

    #apply Tmat    
    qT = Tmat @ points.T
    points = qT.T 

    return points

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # cv2.circle(img,(x,y), 100,(255,0,0),-1)
        x = np.random.randint(100,1500)
        y = np.random.randint(100,1500)
        size = np.random.randint(10, 200)
        rot = np.random.randint(10,150)
        #star1
        points = getRegularPentagon()
        points = makeRmat(rot, points)
        points = points * size
        points[:, 0] += x
        points[:, 1] += y
        points = points.astype('int')
        color = np.random.randint(0, 256, size=3)
        drawStars(canvas, points, color)

        #star2
        points = getRegularPentagon()
        points = makeRmat(rot + 50, points)
        points = points * size
        points[:, 0] += x
        points[:, 1] += y
        points = points.astype('int')
        color = np.random.randint(0, 256, size=3)
        drawStars(canvas, points, color)

def main():
    width, height = 2000, 2000
    canvas = np.zeros( (height, width, 3), dtype='uint8')
    cnt = 0
    while True:
        
        cnt+=1

        if cnt < 30: 
            x = np.random.randint(100,1500)
            y = np.random.randint(100,1500)
            size = np.random.randint(10, 200)
            #star1
            points = getRegularPentagon()
            points = makeRmat(15, points)
            points = points * size
            points[:, 0] += x
            points[:, 1] += y
            points = points.astype('int')
            color = np.random.randint(0, 256, size=3)
            drawStars(canvas, points, color)

            #star2
            points = getRegularPentagon()
            points = makeRmat(60, points)
            points = points * size
            points[:, 0] += x
            points[:, 1] += y
            points = points.astype('int')
            color = np.random.randint(0, 256, size=3)
            drawStars(canvas, points, color)


  


        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: break
        

    #
#


if __name__ == "__main__": # __ 
    main()