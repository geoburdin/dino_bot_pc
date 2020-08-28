from PIL import ImageGrab, Image
import time
import cv2
import pyautogui
import numpy as np

pyautogui.FAILSAFE = False


def find_mana(smth_to_find, where_find, threshold):
    img = cv2.imread(where_find, 0)
    template = cv2.imread(smth_to_find, 0)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # Get the best match position from the match result.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    top_left = (0, 0)
    if max_val >= threshold:
        top_left = max_loc
    return top_left


def take_screen():
    im = ImageGrab.grab(bbox=(0, 0, 600, 1000))
    im.save('screenshot' + '.png', 'PNG')


def map(x, x2):

    im = Image.open('screenshot.png')
    im2 = im.crop((x[0], x[1], x2[0], x2[1]))
    im2.save('map'+'.png', 'PNG')
    img = cv2.imread('map.png')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([13, 150, 150])
    upper_range = np.array([25, 255, 255])

    mask1 = cv2.inRange(hsv, lower_range, upper_range)

    cv2.imwrite('mask1.png', mask1)

    img = cv2.imread('map.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_range = np.array([40, 130, 130])
    upper_range = np.array([80, 255, 255])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    cv2.imwrite('mask2.png', mask)


def offers(mail, pack):

    for i in range(5):
        take_screen()
        print(i)
        map(mail, pack)
        point = find_mana('offers.png', 'mask1.png', 0.61)
        if point != (0, 0):
            print('I`ve found one')
            pyautogui.moveTo(
                mail[0] + point[0] + 15,
                mail[1] + point[1] + 10)
            pyautogui.click()
            time.sleep(2)

            take_screen()
        point = find_mana('offers_green.png', 'mask2.png', 0.61)
        if point != (0, 0):
            print('I`ve found one')
            pyautogui.moveTo(
                mail[0] + point[0] + 15,
                mail[1] + point[1] + 10)
            pyautogui.click()
            time.sleep(2)

            take_screen()
        q = 0
        while find_mana('main.png', 'screenshot.png', 0.8) == (0, 0):
            pyautogui.click()
            q=q+1
            if q>6:
                break
            time.sleep(1.5)
            take_screen()

        if find_mana('cancel.png', 'screenshot.png', 0.7) != (0, 0):
            pyautogui.moveTo(find_mana('cancel.png', 'screenshot.png', 0.7)[0] + 10,
                             find_mana('cancel.png', 'screenshot.png', 0.7)[1] + 10)
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(mail[0], pyautogui.size()[1] / 2)
            pyautogui.mouseDown()
            pyautogui.moveTo(mail[0] + 150, pyautogui.size()[1] / 2, 1,
                             pyautogui.easeInQuad)
            pyautogui.mouseUp()


def map_dino(x, x2):
    im = Image.open('screenshot.png')
    im2 = im.crop((x[0], x[1], x2[0], x2[1]))
    im2.save('map' + '.png', 'PNG')
    img = cv2.imread('map.png')

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_range = np.array([0, 0, 0])
    upper_range = np.array([365, 120, 120])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    cv2.imwrite('mask_dino.png', mask)

def map_mov(img1, img2):
    image1 = cv2.imread(img1)
    image2 = cv2.imread(img2)

    # compute difference
    difference = cv2.subtract(image1, image2)

    # color the mask red
    Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    difference[mask != 255] = [0, 0, 255]

    # store images

    cv2.imwrite('diff.png', difference)


def dino(x, x2):

    for i in range(5):
        take_screen()
        print(i)
        map_dino(x, x2)

        point_col = find_mana('dino.png', 'mask_dino.png', 0.01)
        im = ImageGrab.grab(bbox=(0, 0, 600, 1000))

        im.save('screenshot1' + '.png', 'PNG')

        map_mov('screenshot.png', 'screenshot1.png')
        im = Image.open('diff.png')
        im2 = im.crop((x[0], x[1], x2[0], x2[1]))
        im2.save('diff' + '.png', 'PNG')
        point_mov = find_mana('dino_mov.png', 'diff.png', 0.01)
        if point_col != (0, 0) and point_mov != (0, 0) and abs(point_col[0] - point_mov[0])<60 and abs(point_col[1] - point_mov[1])<60:
            point = ((point_col[0] + point_mov[0])/2, (point_col[1] + point_mov[1])/2)

            print('I`ve found one dino')
            pyautogui.moveTo(
                x[0] + point[0] + 20,
                x[1] + point[1] + 10
                            )
            pyautogui.click()
            time.sleep(2)
            take_screen()
        if find_mana('cancel.png', 'screenshot.png', 0.7) != (0, 0):
            pyautogui.moveTo(find_mana('cancel.png', 'screenshot.png', 0.7)[0] + 10,
                             find_mana('cancel.png', 'screenshot.png', 0.7)[1] + 10)
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(x[0], pyautogui.size()[1] / 2)
            pyautogui.mouseDown()
            pyautogui.moveTo(x[0] + 150, pyautogui.size()[1] / 2, 1,
                             pyautogui.easeInQuad)
            pyautogui.mouseUp()


def analys():
    while True:
        try:
            take_screen()
            if find_mana('mail.png', 'screenshot.png', 0.7) != (0, 0):
                mail = (
                    find_mana('mail.png', 'screenshot.png', 0.7)[0] + 50,
                    find_mana('mail.png', 'screenshot.png', 0.7)[1] + 130,
                )
                pack = (
                    find_mana('pack.png', 'screenshot.png', 0.7)[0] - 20,
                    find_mana('pack.png', 'screenshot.png', 0.7)[1] - 30
                )
                print('Searching for cubes')
                offers( mail, pack)
                print('Searching for dinos')
                dino(mail, pack)
            take_screen()
            if find_mana('main.png', 'screenshot.png', 0.7) != (0, 0):
                pyautogui.moveTo(mail[0] + 50, pyautogui.size()[1] / 2)
                pyautogui.mouseDown()
                pyautogui.moveTo(mail[0] + 150, pyautogui.size()[1] / 2, 1,
                                 pyautogui.easeInQuad)
                pyautogui.mouseUp()

        except Exception as e:
            print(e)
            time.sleep(1)


if __name__== '__main__':
    analys()
