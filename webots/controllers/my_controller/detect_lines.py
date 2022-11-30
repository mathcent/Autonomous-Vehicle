
import cv2
import numpy as np
from sklearn.linear_model import HuberRegressor, Ridge

def get_lower_x(p1,p2):
    m = (p1[1]-p2[1])/(p1[0]-p2[0])
    b = (p1[0]*p2[1]-p2[0]*p1[1])/(p1[0]-p2[0])
    return -b/m #esse é o x para y = 0


def get_center(p1,p2):
    x = (p1[0]+p2[0])/2
    y = (p1[1]+p2[1])/2
    p = [x,y]
    return p


def calculate_intersection(p1,p2,p3,p4):
    c2x = p3[0] - p4[0] 
    c3x = p1[0] - p2[0]
    c2y = p3[1] - p4[1]
    c3y = p1[1] - p2[1]

    d  = c3x * c2y - c3y * c2x

    u1 = p1[0] * p2[1] - p1[1] * p2[0] 
    u4 = p3[0] * p4[1] - p3[1] * p4[0]

    px = (u1 * c2x - c3x * u4) / d
    py = (u1 * c2y - c3y * u4) / d

    p = [px, py ]

    return p

def calcula_erro(p1,p2,p3,p4):
    p_intersection = calculate_intersection(p1,p2,p3,p4)
    p_center = get_center(p2,p4)

    return get_lower_x(p_intersection,p_center)


def draw_lines(img, lines):
        line_dict = {'left':[], 'right':[]}
        img_center = img.shape[1]//2
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1<img_center and x2<img_center:
                    position = 'left'
                elif x1>img_center and x2>img_center:
                    position = 'right'
                else:
                    continue
                line_dict[position].append(np.array([x1, y1]))
                line_dict[position].append(np.array([x2, y2]))
        
        
        
        for position, lines_dir in line_dict.items():
            data = np.array(lines_dir)
            data = data[data[:, 1] >= np.array(15)-1]
            x, y = data[:, 0].reshape((-1, 1)), data[:, 1]

            try:
                model = HuberRegressor(fit_intercept=True, alpha=0.0, max_iter=100,
                                    epsilon=1.9)
                model.fit(x, y)
                
            except ValueError:
                model = Ridge(fit_intercept=True, alpha=0.0, random_state=0, normalize=True)
                model.fit(x, y)

            epsilon = 1e-10
            y1 = np.array(img.shape[0])
            x1 = (y1 - model.intercept_)/(model.coef_+epsilon)
            y2 = np.array(15)
            x2 = (y2 - model.intercept_)/(model.coef_+epsilon)
            x = np.append(x, [x1, x2], axis=0)

            y_pred = model.predict(x)
            data = np.append(x, y_pred.reshape((-1, 1)), axis=1)
            if position == 'left':
                p1 = [x[-1],y_pred.reshape((-1, 1))[-1]]
                p2 = [x[-2],y_pred.reshape((-1, 1))[-2]]
            else:
                p3 = [x[-1],y_pred.reshape((-1, 1))[-1]]
                p4 = [x[-2],y_pred.reshape((-1, 1))[-2]]
        erro  = calcula_erro(p1,p2,p3,p4)-(img.shape[1])/2
        return erro
        


def criaImagem(image):
    
    grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    kernel_size = 5

    blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
    
    slice1Copy = (blur*255).astype(np.uint8)
    edges  = cv2.Canny(slice1Copy, 200, 300)

    #Create a set of vertices for the mask (1270,780),(0,780),(10,450),(1270,460)
    x1=image.shape[1]
    x2=0
    x3=(2*image.shape[1])/6
    x4=(4*image.shape[1])/6
    y1=image.shape[0]
    y2=image.shape[0]
    y3=(6*image.shape[0])/10
    y4=(6*image.shape[0])/10


    vertices = np.array([[(x1,y1), (x2,y2), (x3,y3), (x4,y4)]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    rho = 3
    theta = np.pi / 180
    threshold = 15
    min_line_len = 30
    max_line_gap = 40


    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((masked_edges.shape[0], masked_edges.shape[1], 3), dtype=np.uint8)
    return  draw_lines(line_img,lines)
     
    










