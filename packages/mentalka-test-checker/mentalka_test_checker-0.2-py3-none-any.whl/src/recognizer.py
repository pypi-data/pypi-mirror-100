import cv2
from read_cell import make_it
from qr_table1_table2 import take_it
from preprocessing import clever_resize
from paint_orign import paint_marks
from read_qrcode import read_qrcode
from setting import logger
import numpy as np

def check(image):
    try:
        if type(image) != type(np.array([])):
            image = np.array(image)
        qr_code = read_qrcode(image)
        qr_code = 'v9x10_blankinfo_childinfo' #
        blank_type = qr_code.split('_')[0]
        image, scans, rects = take_it(image, blank_type)
        result = make_it(scans, blank_type)
        logger.info('Распознование проведено!')
        return result, scans, rects, blank_type, qr_code
    except Exception as ex:
        logger.warning(f'Ошибка при проверке бланка {ex}')


def paint(image, all_marks, rects, blank_type):
    if isinstance(image, np.ndarray):
        image = np.array(image)
    for i, marks in enumerate(all_marks):
        image = paint_marks(image, rects[i], marks, blank_type)
    logger.info('Разметка проведена!')
    return image



if __name__ == '__main__':
    # параметр для сканируемого изображения
    args_image = 'data/v9.jpg'
    # прочитать изображение
    image = cv2.imread(args_image)
    image = clever_resize(image)
    result, scans, rects, blank_type, qr_code = check(image)
    marks1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    marks2 = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1]
    all_marks = [marks1, marks2]
    painted_image = paint(image, all_marks, rects, blank_type)
    cv2.imshow('painted_img', painted_image)
    print(result)
    print(qr_code)
    cv2.waitKey(0)  # press 0 to close all cv2 windows
    cv2.destroyAllWindows()
































# # if __name__ == '__main__':
#
# #     #make_it('PyCharm')
