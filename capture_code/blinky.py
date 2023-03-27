#blinky.py
#kekim@hmc.edu
import board
import time
import adafruit_dotstar as dotstar

def main():
    
    N_dots = 8*8
    dots = dotstar.DotStar(board.SCK, board.MOSI, N_dots, brightness = 0.055)
    for i in range(8):
        for j in range(8):
            dots[i*8 + j] = (0,255,0)

def showPixel(x,y):
    N_dots = 8*8
    dots = dotstar.DotStar(board.SCK, board.MOSI, N_dots, brightness = 0.055)
    led_idx = 8*x + y
    dots[led_idx] = (255,0,0)
def killPixels():
    N_dots = 8*8
    dots = dotstar.DotStar(board.SCK, board.MOSI, N_dots, brightness = 0.05)
    dots[0] = (0,0,0)

main()

