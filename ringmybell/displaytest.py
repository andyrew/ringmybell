import time
import board
from adafruit_ht16k33.segments import Seg14x4

i2c = board.I2C()
display1 = Seg14x4(i2c, address=0x70)
display1.print("ABCD")
display2 = Seg14x4(i2c, address=0x71)
display2.print("EFGH")
display3 = Seg14x4(i2c, address=0x72)
display3.print("IJKL")
display4 = Seg14x4(i2c, address=0x73)
display4.print("MNOP")

time.sleep(2)

display1.print("    ")
display2.print("    ")
display3.print("    ")
display4.print("    ")

time.sleep(0.5)

display1.set_digit_raw(1, 0b0000000000100001)
display2.set_digit_raw(1, 0b0000000000100001)
