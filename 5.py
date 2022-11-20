import numpy as np
import cv2


def get_block(h=30, w = 120):
    block_vertices = np.array([[0,h,1], [0, 0, 1], [w,0,1], [w, h, 1]])
    return block_vertices


def getline(x0, y0, x1, y1):
    points = []
    inclination = 0
    if x0 != x1:
        inclination =  (y0-y1) / (x0-x1)
    

    if (inclination > 1) or (inclination < -1):
        if y0 > y1:
            for y in range(y1, y0-1, 1):
                x = (y-y0)*(x1-x0)/(y1-y0) + x0
                # print(f"x: {x}, y: {y}")
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



def drawLine(canvas, p, q, color=(255, 255, 255)):
    x0, y0, x1, y1 = p[0], p[1], q[0], q[1]
    xys = getline(x0, y0, x1, y1)
    
    for xy in xys:
        x, y = xy
        canvas[y, x] = color
    return
#

def getRect(width, height):
    points = []
    points.append( (-width/2,0) )
    points.append( (width/2,0) )
    points.append( (width/2,height) )
    points.append( (-width/2, height) )

    points = np.array(points)
    return points

def RectJoint(pts):
    return np.array(((pts[2][0] + pts[3][0])/2, (pts[2][1] + pts[3][1])/2))

def angleBetweenVector(v1,v2):
    uvec2 = v1 / np.linalg.norm(v1)
    uvec2 = v2 / np.linalg.norm(v2)
    return np.arctan(np.cross(uvec1, uvec2), np.dot(uvec1, uvec2))

def invKinematics(current, tip, goal, angle):
    angle += angleBetweenVector((tip-current), (goal-current))
    return angle

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad 

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


def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 

def drawPolygon(canvas, pts, color):

    pts = pts.astype('int')

    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k], pts[k+1], color)
        
    # for k in range(pts.shape[0]-2):
    #     drawLine(canvas, pts[k,0], pts[k,1], pts[k+2,0], pts[k+2,1], color)
        
    # for k in range(pts.shape[0]-3):
    #     drawLine(canvas, pts[k,0], pts[k,1], pts[k+3,0], pts[k+3,1], color)

    drawLine(canvas, pts[-1], pts[0], color)
                    
    # drawLinePQ(canvas, pts[-1], pts[0], color)

    return 


def makeRmat(degree):
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)

    #make Rmat
    Rmat = np.eye(3)
    Rmat[0,0] = c
    Rmat[0,1] = -s
    Rmat[1,0] = s
    Rmat[1,1] = c
    
    #calculate Rmat
    # qT = Rmat @ points.T
    # points = qT.T 
    return Rmat 


def makeTmat(tx, ty):
    #make Tmat
    Tmat = np.eye(3)
    Tmat[0,2] = tx
    Tmat[1,2] = ty

    # #apply Tmat    
    # qT = Tmat @ points.T
    # points = qT.T 

    return Tmat

def erase(canvas):
    canvas[:,:,:] = (0,0,0)
    return canvas

def main():
    height, width = 600, 1000
    

    block_height, block_width = 120, 30
    block = get_block(block_height, block_width).T

    T0 = makeTmat(width/2, height - block_height -1)
    T1 = makeTmat(-block_width/2, -block_height)
    T2 = makeTmat(block_width/2, block_height)
    T3 = makeTmat(0, -block_height)

    degree1 = 0
    degree2 = 0
    degree3 = 0

    v1 = 5
    v2 = 7
    v3 = 9

    while True:
        window = np.zeros( (height, width, 3), dtype='uint8')

        

        R1 = makeRmat(degree1)
        R2 = makeRmat(degree2)
        R3 = makeRmat(degree3)

        H1 = T0
        block1 = (H1 @ block).T
        drawPolygon(window, block1, (255, 255, 255))

        H2 = T3 @ T2 @ R1 @ T1
        block2 = (H1 @ H2 @ block).T
        drawPolygon(window, block2, (255,100,255))

        H3 = T3 @ T2 @ R2 @ T1
        block3 = (H1 @ H2 @ H3 @ block).T
        drawPolygon(window, block3, (255,100,100))

        H4 = T3 @ T2 @ R3 @ T1
        block4 = (H1 @ H2 @ H3 @ H4 @ block).T
        drawPolygon(window, block4, (100,100,100))
        
        if degree1 >= 15 or degree1 <= 15:
            v1 = -v1
        if degree2 >= 30 or degree2 <= 30:
            v2 = -v2
        if degree3 >= 45 or degree3 <= 45:
            v3 = -v3
        degree1 += v1
        degree2 += v2
        degree3 += v3
        

        cv2.imshow("display", window)
        if cv2.waitKey(10) == 27: break

    return


if __name__ == "__main__": # __ 
    main()