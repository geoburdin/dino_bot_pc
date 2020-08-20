from PIL import ImageGrab
import time
import cv2
import pyautogui
import numpy as np

pyautogui.FAILSAFE = False


def find_mana(smth_to_find, where_find):
    img = cv2.imread(where_find, 0)
    template = cv2.imread(smth_to_find, 0)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # Get the best match position from the match result.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.5
    top_left = (0, 0)
    if max_val >= threshold:
        top_left = max_loc
    return top_left


def take_screen():
    im = ImageGrab.grab(bbox=(0, 0, 800, 1000))
    im.save('screenshot' + '.png', 'PNG')


def map(x,x2):
    if find_mana('mail.png', 'screenshot.png') != (0, 0):
        im = ImageGrab.grab(bbox=(x[0], x[1], x2[0], x2[1]))
        im.save('map.png', 'PNG')
        img = cv2.imread('map.png')

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_range = np.array([13, 150, 150])
        upper_range = np.array([25, 255, 255])

        mask = cv2.inRange(hsv, lower_range, upper_range)

        cv2.imwrite('mask.png', mask)


def offers(offer, mail, pack):
    for i in range(5):
        take_screen()
        print(i)
        map(mail, pack)
        point = find_mana(offer, 'mask.png')
        if point != (0, 0):
            print('I`ve found one')
            pyautogui.moveTo(
                mail[0] + point[0] + 15,
                mail[1] + point[1] + 10)
            pyautogui.click()
            time.sleep(3)
            pyautogui.click()
            take_screen()

        if find_mana('cancel.png', 'screenshot.png') != (0, 0):
            pyautogui.moveTo(find_mana('cancel.png', 'screenshot.png')[0] + 10,
                             find_mana('cancel.png', 'screenshot.png')[1] + 10)
            pyautogui.click()
            take_screen()
        while find_mana('pack.png', 'screenshot.png') == (0, 0):
            pyautogui.click()
            time.sleep(1)
            take_screen()


def analys():
    while True:
        try:
            take_screen()
            if find_mana('mail.png', 'screenshot.png') != (0, 0):
                mail = (
                    find_mana('mail.png', 'screenshot.png')[0] + 50, find_mana('mail.png', 'screenshot.png')[1] + 150,
                )
                pack = (
                    find_mana('pack.png', 'screenshot.png')[0] - 20, find_mana('pack.png', 'screenshot.png')[1] - 30
                )
                offers('offers.png', mail, pack)

            if find_mana('main.png', 'screenshot.png') != (0, 0):
                pyautogui.moveTo(find_mana('mail.png', 'screenshot.png')[0], pyautogui.size()[1] / 2)
                pyautogui.mouseDown()
                pyautogui.moveTo(find_mana('mail.png', 'screenshot.png')[0] + 100, pyautogui.size()[1] / 2, 1,
                                 pyautogui.easeInQuad)
                pyautogui.mouseUp()

        except Exception as e:
            print(e)
            time.sleep(1)


analys()
