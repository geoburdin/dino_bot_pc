from PIL import ImageGrab
import time
import cv2
import pyautogui
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'Tesseract-OCR'


def find_mana(smth_to_find, where_find):
    img = cv2.imread(where_find, 0)
    template = cv2.imread(smth_to_find, 0)
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # Get the best match position from the match result.
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.6
    top_left = (0, 0)
    if max_val >= threshold:
        top_left = max_loc
    return top_left


def main():

    im = ImageGrab.grab()
    im.save('screenshot' + '.png', 'PNG')
    print('I`m looking')


def offers(offer):
    if find_mana(offer, 'screenshot.png') != (0, 0):
        print('I`ve found one')
        pyautogui.moveTo(find_mana(offer, 'screenshot.png')[0] + 5,
                         find_mana(offer, 'screenshot.png')[1] + 5)
        pyautogui.click()
        time.sleep(5)
        pyautogui.click()
        main()
        while find_mana('main.png', 'screenshot.png') == (0, 0) and find_mana('cancel.png', 'screenshot.png') == (0, 0):
            time.sleep(3)
            pyautogui.click()
        if find_mana('cancel.png', 'screenshot.png') != (0, 0):
            pyautogui.moveTo(find_mana('cancel.png', 'screenshot.png')[0] + 10,
                             find_mana('cancel.png', 'screenshot.png')[1] + 10)
            pyautogui.click()
        no_offers = False
        main()

def analys():

    pyautogui.FAILSAFE = False
    take_pic = True

    while take_pic == True:
        try:
            main()
            no_offers = True
            offers('offers.png')
            offers('offers1.png')
            offers('offers2.png')
            if find_mana('main.png', 'screenshot.png') != (0, 0) and no_offers == True:
                print('I`m moving')
                pyautogui.moveTo(100, pyautogui.size()[1]/2)
                pyautogui.mouseDown()
                pyautogui.moveTo(200, pyautogui.size()[1]/2, 1, pyautogui.easeInQuad)
                pyautogui.mouseUp()
                main()

        except Exception as e:
            time.sleep(1)

analys()