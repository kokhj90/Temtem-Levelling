import pyautogui
from time import sleep
import os
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Apps\\Tesseract-OCR\\tesseract.exe"  # location of tesseract.exe

DELAY_BETWEEN_COMMANDS = 0.8
TEM_INTEREST = "cycrox.png"     # looking for a specific tem
N_KO = 2 # no. of ko-ed tem                          

def main():
    initializePyAutoGUI()
    countdownTimer()
    
    tS = trainerStatus()

    while 1:
        if tS.n_ko>=N_KO:
            # double check at this pointd
            sleep(DELAY_BETWEEN_COMMANDS)
            pyautogui.press("escape")
            sleep(DELAY_BETWEEN_COMMANDS)
            pyautogui.click(105,494,1)
            sleep(DELAY_BETWEEN_COMMANDS)
            tS = readHealth(tS,False)
            sleep(DELAY_BETWEEN_COMMANDS)
            pyautogui.press("escape")
            
            print("{} KO-ed, checked at main loop".format(tS.n_ko))
        
            if tS.n_ko>=3:
                if not tS.usedPhial:
                    usePhial()
                    tS.n_ko = 0
                    tS.rdy = 2
                    tS.usedPhial = True
                else:
                    break
        
        sleep(DELAY_BETWEEN_COMMANDS)
        isWorldScreen = checkWorldScreen()
        
        if isWorldScreen:
            tS = startEncounter(tS)
            
#    reportMousePosition()
# =============================================================================
#     checkLuma()
# =============================================================================

    print("Done")
        
class trainerStatus:
    def __init__(self):
        self.n_ko = 0
        self.usedPhial = False   
        self.isLuma = False
        self.rdy = 2            # refers to the third temtem, who is presumably healthy at this point
    
def initializePyAutoGUI():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.htmwl
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True

def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 3):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")

def reportMousePosition(seconds=10):
    for i in range(0, seconds):
        print(pyautogui.position())
        sleep(1)
        
def startEncounter(tS):
    while 1:
        # Move left and right
        holdKey('a', 0.30)
        holdKey('d', 0.30)
        # Check if entered encounter
        isBattleScreen = checkBattleScreen()
        
        if isBattleScreen:
            isLuma = checkLuma()
            isInterest = checkInterest()
            if isLuma or isInterest:
                userPlay()
            else:
                tS = stayInBattle(tS)
            break 
            
    return tS

def userPlay():
    while 1:
        isWorldScreen = checkWorldScreen()
        
        if not isWorldScreen:
            break
    
        
def readHealth(tS,swap):
    width = 140
    height = 40
    hp_positions = [[1110,349],[2260,509],[1110,704],[2260,864],[1110,1058]]
    n_ko=0
    
    #cnt=1
    for i in hp_positions:
        # print("{},{}".format(i[0],i[1]))
        im = pyautogui.screenshot(region=(i[0],i[1],width,height))
        # cnt=cnt+1
        hp_str = pytesseract.image_to_string(im)
        print(hp_str)
        ind = hp_str.find("/")
        if ind==-1:
            continue
        else:
            if float(hp_str[0:ind])==0:
                n_ko=n_ko+1
    
    if swap:
        print("Swapping Now")
        pos = hp_positions[tS.rdy]
        pyautogui.click(pos[0], pos[1], duration=0.1) 
        tS.rdy = tS.rdy+1
    
    tS.n_ko = n_ko
    
    return tS
        
def stayInBattle(tS):
    # Check once more
    isBattleScreen = checkBattleScreen()
    if isBattleScreen:
        #print("run twice")
        #runTwice()
       print("use first skill twice")
       useFirstSkillTwice()
    # if a temtem is knocked out and needs replacement    
    tS = checkHealthStatus(tS)  
    
    # if a temtem is prompted to learn a new move   
    checkLearnNewMove()
        
    # check if fight is done and we're back to world screen
    isWorldScreen = checkWorldScreen()
    
    if not isWorldScreen:
        tS = stayInBattle(tS)
    
    return tS

def checkLearnNewMove():
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images',"new_technique.png")
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.8)
    except: 
        print("Not prompted to learn new technique")
    else:
        pyautogui.press("escape")
        sleep(DELAY_BETWEEN_COMMANDS)
        
    return
        
def checkBattleScreen():
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images',"wait_button.png")
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.9)
    except: 
        print("Not at battle screen")
        return False
    else:
        print("At battle screen")
        return True

def usePhial():
    print("Using Phial now")
    sleep(DELAY_BETWEEN_COMMANDS)
    pyautogui.press("escape")
    pyautogui.moveTo(221,376,1)
    sleep(DELAY_BETWEEN_COMMANDS)
    pyautogui.click(239,643,1)
    sleep(DELAY_BETWEEN_COMMANDS)
    
    images_to_check = [
            'tem_phial1.png',
            'tem_phial2.png'
        ]
    
    script_dir = os.path.dirname(__file__)
    
    for img_filename in images_to_check:
        image_path = os.path.join(script_dir,'images',img_filename)
    
        try:
            image_pos = pyautogui.locateOnScreen(image_path, confidence=0.9)
        except: 
            print("Not sure what happened")
            continue
        else:
            pyautogui.click(image_pos[0]+50, image_pos[1]+50)
            sleep(DELAY_BETWEEN_COMMANDS)
            pyautogui.press("f")
            sleep(2)
            pyautogui.press("escape")
            sleep(1)
            break
            
    return
                
def checkHealthStatus(tS):
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images',"large_bars.png")
    
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.8)
    except: 
        print("Not prompted to swap temtem")
        return tS
    else:
        tS = readHealth(tS,True)
        print("{} knocked out".format(tS.n_ko))
        sleep(1)
        return tS
        
def checkWorldScreen():
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images',"local_chat_icon_02.png")
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.9)
    except: 
        print("Not at world screen -> checking battle screen")
        return False
    else:
        print("At world screen")
        return True
        
def useFirstSkillTwice():
    pyautogui.click(352, 1389)
    sleep(DELAY_BETWEEN_COMMANDS)
    pyautogui.press("f")
    sleep(1)
    pyautogui.click(352, 1389)
    sleep(DELAY_BETWEEN_COMMANDS)
    pyautogui.press("f")
    sleep(10)
    
def runTwice():
    pyautogui.click(1256, 1389)
    sleep(DELAY_BETWEEN_COMMANDS)
    sleep(1)
    pyautogui.click(1256, 1389)
    sleep(DELAY_BETWEEN_COMMANDS)
    sleep(5)
    
def holdKey(key, seconds=1.00):
    pyautogui.keyDown(key)
    sleep(seconds)
    pyautogui.keyUp(key)
    sleep(DELAY_BETWEEN_COMMANDS)

def checkInterest():
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images_tem',TEM_INTEREST)
    
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.8)
    except: 
        print("Not temtem of interest")
        return False
    else:
        print("Temtem found")
        sleep(1)
        return True
    
def checkLuma():
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir,'images',"luma_icon.png")
    try:
        image_pos = pyautogui.locateOnScreen(image_path, confidence=0.7)
    except: 
        print("Not luma")
        return False
    else:
        if image_pos:
            print("Is luma")
            return True
    
if __name__ == "__main__":
    main()
