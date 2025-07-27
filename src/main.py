from playerBehavior import *
from playerObservation import *
from script import *
import time


def forge():
    print("forge")
    bag1 = (895, 1025)
    bag2 = (960, 1025)
    craft1 = (1032, 818)
    craft2 = (1400, 818)
    # 合成
    mouseClick(*bag1)
    mouseClick(*craft1)
    time.sleep(0.1)
    mouseClick(*craft2)
    mouseClick(*bag2)
    mouseClick(*craft1)
    mouseClick(*bag1)
    keyboardPress("e")
    # 锻造
    bag1 = (1000, 760)
    bag2 = (1068, 760)
    forge1 = (1075, 614)
    forge2 = (1270, 614)
    forge3 = (1500, 610)
    mouseRightClick()
    time.sleep(0.1)
    mouseClick(*bag1)
    mouseClick(*forge1)
    mouseClick(*bag2)
    mouseClick(*forge2)
    time.sleep(0.1)
    mouseClick(*forge3)
    mouseClick(*bag1)
    keyboardPress("e")
    time.sleep(0.1)
    keyboardPress("\\")
    time.sleep(0.1)


def check_item(_debug=False):
    threshold = 0.43
    while True:
        img = screen_shot()
        item = img[384:604, 1052:1120]
        item1 = item[0:68]
        item2 = item[76:144]
        item3 = item[152:220]

        target = img[792:856, 1320:1384]
        like1 = img_match(target, item1)
        like2 = img_match(target, item2)
        like3 = img_match(target, item3)
        print(round(like1, 6), round(like2, 6), round(like3, 6))
        # print(target[0][0])
        if _debug:
            # mouseClick()
            break
        elif like1 > threshold:
            return 1
        elif like2 > threshold:
            return 2
        elif like3 > threshold:
            return 3
        else:
            mouseClick()


def trans_table():
    target_item = (1285, 825)  # 目标物品
    replaced_item = (1285, 1060)  # 用于替换的物品
    table_item = (1300, 685)  # 嬗变台当前的物品
    trans_item1 = (1445, 425)  # 可嬗变的物品
    trans_item2 = (1445, 500)
    trans_item3 = (1445, 575)
    outside = (1825, 685)
    # 往嬗变台里面放两个物品
    mouseClick(*target_item)
    mouseRightClick(*table_item)
    mouseRightClick(*table_item)
    mouseClick(*target_item)
    # 嬗变一次
    mouseClick(*trans_item2)
    mouseRightClick(*table_item)
    mouseClick(*outside)
    # 开始嬗变
    mouseMoveTo(*trans_item2)
    item_pos = check_item()
    # 根据目标物品位置替换
    mouseClick(*replaced_item)
    mouseClick(*table_item)
    mouseClick(*outside)
    if item_pos == 1:
        mouseClick(*trans_item1)
    elif item_pos == 2:
        mouseClick(*trans_item2)
    elif item_pos == 3:
        mouseClick(*trans_item3)
    mouseClick(*table_item)
    mouseClick(*outside)


def level_get():
    en_1 = (1060, 545)
    en_2 = (1280, 545)
    en_3 = (1490, 545)
    mouseClick(*en_3)
    mouseClick(*en_1)
    mouseClick(*en_2)
    time.sleep(0.1)


DEBUG = 0

if __name__ == "__main__":
    if DEBUG:
        pyautogui.mouseInfo()
    else:
        print("start")
        loop = LoopFunction("p", "`", level_get)
        # loop = LoopFunction("p", "`", forge)
        # add_hotkey("l", trans_table)
        # add_hotkey("l", check_item, args=(True,))
        keyboard.wait("esc")
