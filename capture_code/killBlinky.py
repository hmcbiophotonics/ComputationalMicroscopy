#killBlinky.py
#kekim@hmc.edu
import board
import time
import adafruit_dotstar as dotstar

def main():
    
    N_dots= 8*8
    dots = dotstar.DotStar(board.SCK, board.MOSI, N_dots, brightness = 0.000)
    for i in range(8):
        for j in range(8):
            dots[8*i+j] = (0,0,0)
main()
