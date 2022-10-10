from ctypes import sizeof
from operator import index
import sys
import math
from tokenize import Ignore
import cv2
import numpy as np

def main(argv):
    
    # Loads an image
    image = cv2.imread('TCC_DETEC_LINHAS\RETA.png')
    # Check if image is loaded fine
    
    if image is None:
        print ('Error opening image!')
        return -1

    #frame into grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    ##Gaussian blur to the frame
    kernel_size = 5
    blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
    
    ##Canny edge detection
    edges  = cv2.Canny(blur, 50, 150)

    #Create a set of vertices for the mask (0, image.shape[0]), (0, 1280), (790, 0), (image.shape[1], image.shape[0])
    vertices = np.array([[(1270,780),(0,780),(10,450),(1270,460)]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    rho = 3
    theta = np.pi / 180
    threshold = 15
    min_line_len = 150
    max_line_gap = 60
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    delete = []
    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            ##ignorar a linha do meio
            if(l[0] > 500 and l[0] < 700 and l[1] > 440 and l[1] < 781  and l[2] > 500 and l[2] <700 and l[3] > 440 and l[3] <781 ):
                delete.append(i)
            else:
                cv2.line(masked_edges, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)


        

    ##cv2.imshow("grayscale", grayscale)
    ##cv2.imshow("blur", blur)
    ##cv2.imshow("edges", edges)
    ##cv2.imshow("mask", mask)
    print(lines)
    cv2.imshow("image", image)
    cv2.imshow("masked_edges", masked_edges)
    ##cv2.imshow("edges", edges)
    cv2.waitKey()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])