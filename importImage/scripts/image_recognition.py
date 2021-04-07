import cv2
import numpy as np


class ImageRecognition():

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        self.rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def take_metadata(self):
        '''
        получаем требуемую метадату (высоту и ширину изображения)
        :return: height, width
        '''
        height, width = self.image.shape[:2]
        return height, width

    def average_colour(self):
        '''
        выводим средний цвет изображения
        :return: avg_colour в формате RGB
        '''
        avg_colour_per_row = np.average(self.rgb_image, axis=0)
        avg_colour = np.average(avg_colour_per_row, axis=0)
        avg_colour = list(avg_colour)
        return avg_colour

    def count_circles(self):
        '''
        считаем количество кругов (монет) на изображении
        :return: count_coins -> int() - количество кругов (монет) на изображении
        '''
        # загружаем изображение
        img = cv2.imread(self.image_path, 0)
        # преобразовываем его
        img = cv2.medianBlur(img, 31)
        # находим окружности на изображении
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 30,
                                   param1=50, param2=45, minRadius=0, maxRadius=0)

        circles = np.uint16(np.around(circles))
        # считаем их количество
        count_coins = len(circles[0, :])
        return count_coins

    def recognize_coins(self):
        '''
        здесь определяем номинал
        :return:coins_nominal -> dict () {'номинал монеты': количество монет}
        '''
        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        # удаление шума
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(
            thresh,
            cv2.MORPH_OPEN,
            kernel,
            iterations=2
        )
        # фоновая область
        sure_bg = cv2.dilate(
            opening,
            kernel,
            iterations=3
        )
        # поиск нужной области переднего плана
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(
            dist_transform,
            0.7*dist_transform.max(),
            255,
            0
        )

        # поиск неизвестного региона
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        ret, markers = cv2.connectedComponents(sure_fg)

        # добавляем 1 ко всем ярлыкам, чтобы фон был не 0, а 1
        markers = markers + 1

        # теперь отмечяем область неизвестного 0
        markers[unknown==255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]
        return None


        # coins_nominal = {
        #     'one_ruble': 0,
        #     'two_ruble': 0,
        #     'five_ruble': 0,
        #     'ten_ruble': 0,
        # }
        # return coins_nominal