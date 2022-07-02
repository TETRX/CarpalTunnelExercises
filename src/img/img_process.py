import cv2
import numpy as np


def get_img(path,desired_x=200, desired_y = 200):
    img = cv2.imread(path)

    height,width,_ = img.shape
    max_side = max(width,height)
    img = cv2.copyMakeBorder(img, (max_side-height)//2, (max_side-height)//2, (max_side-width)//2, (max_side-width)//2,
                             cv2.BORDER_CONSTANT, value=[255,255,255])
    img = cv2.resize(img, (desired_x,desired_y))
    return img

if __name__ == '__main__':
    img = get_img("../../img/ex4a/ex4a_1.png")
    cv2.imshow('test', img)
    cv2.waitKey(0)

    #closing all open windows
    cv2.destroyAllWindows()