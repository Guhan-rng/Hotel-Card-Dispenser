i2c_address = 0x7F
i2c_port_num = 1
frequency = 50

from Adafruit_IO import Client
import time
from grovepi import *
import random
import smbus
from RPiPCA9685 import RPiPCA9685
import grovepi
from time import sleep
import math
from sense_hat import SenseHat

pca9685 = RPiPCA9685.PCA9685(i2c_address, i2c_port_num)
pca9685.set_frequency(frequency)

#adafruit feed, command, display
ADAFRUIT_IO_USERNAME = "Goombastein"
ADAFRUIT_IO_KEY = "aio_hhaY48n2cE3Mk2c6Au2RTlPdpwpU"
FEED_KEY = "keypad"
FEED_COMMAND = "admin-control"
FEED_PASSWORD_DISPLAY = "password-display"
FEED_STATUS = "dispenser-status"

#pins
led_blue = 2
led_red = 5
potentiometer = 0
button = 3
ultrasonic = 4
dht_sensor = 6
buzzer = 8


sense = SenseHat()
n = (0, 0, 0) 
b = (0, 0, 255)
y = (255, 255, 0)
o = (255, 127, 0)
r = (255, 94, 5)

MOTOR_1 = 0
MOTOR_2 = 4

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# clear old commands from adafruit, prevent instantly recognising from adafruit
try:
    old_cmd = aio.receive(FEED_COMMAND)
    if old_cmd:
        print(f"cleared old command")
except:
    print("no old commands")

try:
    old_pwd = aio.receive(FEED_PASSWORD_DISPLAY)
    if old_pwd:
        print(f"Cleared old password")
except:
    print("No old password")

# Setup pins
grovepi.pinMode(led_blue, "OUTPUT")
grovepi.pinMode(led_red, "OUTPUT")
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(buzzer, "OUTPUT")

# Setup motors
grovepi.set_bus("RPI_1")

# Setup LCD screen
bus = smbus.SMBus(1)
LCD_COLOR = 0x62
LCD_TEXT = 0x3e

adc_ref = 5
grove_vcc = 5
full_angle = 300

# Global variables
code1 = 0
code2 = 0
system_enabled = True
last_command_value = None
password_locked = True  # Track if password display is locked on LCD
access_count = 0  # Track total number of dispenses

# --- LCD Functions ---
def lcd_color(r, g, b):
    bus.write_byte_data(LCD_COLOR, 0, 0)
    bus.write_byte_data(LCD_COLOR, 1, 0)
    bus.write_byte_data(LCD_COLOR, 0x08, 0xaa)
    bus.write_byte_data(LCD_COLOR, 4, r)
    bus.write_byte_data(LCD_COLOR, 3, g)
    bus.write_byte_data(LCD_COLOR, 2, b)


def lcd_message(text):
    bus.write_byte_data(LCD_TEXT, 0x80, 0x02)
    time.sleep(0.05)
    bus.write_byte_data(LCD_TEXT, 0x80, 0x0C)
    bus.write_byte_data(LCD_TEXT, 0x80, 0x28)
    time.sleep(0.05)
    
    while len(text) < 32:
        text += " "
    count = 0
    row = 0
    for char in text:
        if char == "\n" or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            bus.write_byte_data(LCD_TEXT, 0x80, 0xC0)
            if char == "\n":
                continue
        count += 1
        bus.write_byte_data(LCD_TEXT, 0x40, ord(char))


def send_count_to_admin():
    #Send the dispensing count to Adafruit IO for admin monitoring
    global access_count
    try:
        aio.send(FEED_STATUS, f"COUNT:{access_count}")
        print("send count to admin")
    except Exception as e:
        print(f"Could not send count")

#Generate new random codes for both rooms and send to admin
def generate_random_codes():    
    global code1, code2
    code1 = random.randint(1000, 9999)#get 2 random codes
    code2 = random.randint(1000, 9999)
    while code2 == code1:
        code2 = random.randint(1000, 9999)#justincase both is the same
    try:
        password_message = f"Room1:{code1}|Room2:{code2}"
        aio.send(FEED_PASSWORD_DISPLAY, password_message)#send this to admin
    except Exception as e:
        print(f"Could not send passwords to admin")
    return code1, code2

 #Check if SenseHat joystick center button is pressed for reset
def check_sensehat_reset():
    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "middle":#only middle will work
                print("SENSE HAT JOYSTICK RESET PRESSED - Restarting system...")
                lcd_color(255, 165, 0)
                lcd_message("Resetting...\nPlease wait")
                grovepi.digitalWrite(led_red, 0)
                grovepi.digitalWrite(led_blue, 0)
                time.sleep(0.5)
                lcd_message("")
                return True
    return False

# Display pixel art on SenseHat
def temp():
    [temp, humidity] = grovepi.dht(dht_sensor, 0) 
    if temp > 30 and humidity <= 90:
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, o, o, o, o, n, n,
        n, r, o, y, y, o, r, n,
        n, r, o, y, y, o, r, n,
        n, r, o, y, o, r, n, n,
        n, n, r, o, o, n, n, n,
        n, n, n, r, n, n, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, y, y, n, n, n,
        n, n, y, y, y, y, n, n,
        n, n, y, y, y, y, n, n,
        n, n, n, y, y, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)

    elif temp <= 30 and humidity <= 90:
        creeping_pixels = [
        b, n, n, b, b, n, n, b,
        n, b, n, b, b, n, b, n,
        n, n, b, b, b, b, n, n,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        n, n, b, b, b, b, n, n,
        n, b, n, b, b, n, b, n,
        b, n, n, b, b, n, n, b
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)
        
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, y, y, n, n, n,
        n, n, y, y, y, y, n, n,
        n, n, y, y, y, y, n, n,
        n, n, n, y, y, n, n, n,
        n, n, n, n, n, n, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)

    elif temp > 30 and humidity > 90:
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, o, o, o, o, n, n,
        n, r, o, y, y, o, r, n,
        n, r, o, y, y, o, r, n,
        n, r, o, y, o, r, n, n,
        n, n, r, o, o, n, n, n,
        n, n, n, r, n, n, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, n, y, n, n, n, n,
        n, n, n, n, y, n, n, n,
        n, n, n, y, n, n, n, n,
        n, b, b, b, b, b, b, n,
        n, b, b, b, b, b, n, n,
        n, n, n, b, b, b, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)

    elif temp <= 30 and humidity > 90:
        creeping_pixels = [
        b, n, n, b, b, n, n, b,
        n, b, n, b, b, n, b, n,
        n, n, b, b, b, b, n, n,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        n, n, b, b, b, b, n, n,
        n, b, n, b, b, n, b, n,
        b, n, n, b, b, n, n, b
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)
        creeping_pixels = [
        n, n, n, n, n, n, n, n,
        n, n, n, y, n, n, n, n,
        n, n, n, n, y, n, n, n,
        n, n, n, y, n, n, n, n,
        n, b, b, b, b, b, b, n,
        n, b, b, b, b, b, n, n,
        n, n, n, b, b, b, n, n,
        n, n, n, n, n, n, n, n
        ]
        sense.set_pixels(creeping_pixels)
        time.sleep(2)
    time.sleep(4)







#receive commands from admin
def check_adafruit_commands():
    global system_enabled, last_command_value, password_locked
    try:
        cmd_data = aio.receive(FEED_COMMAND)
        if cmd_data and cmd_data.value:
            cmd = cmd_data.value
            
            if cmd == last_command_value:# Avoid processing the same command multiple times
                return
            
            last_command_value = cmd
            
            
            if cmd == "SYSTEM_STOP":
                system_enabled = False
                print("System disabled by admin")
                lcd_color(255, 0, 0)
                lcd_message("SYSTEM disabled\nby Admin")
                time.sleep(2)
                
            elif cmd == "SYSTEM_START":
                system_enabled = True
                print("System enabled by admin")
                lcd_color(0, 255, 0)
                lcd_message("System enabled \nby admin")
                time.sleep(2)
                
            elif cmd == "PASSWORD_LOCK":
                # Lock password display on LCD (admin GUI still shows passwords)
                password_locked = True
                print("Password lock by admin")
                lcd_color(255, 0, 0)
                lcd_message("LCD Locked\nby admin")
                time.sleep(2)
                
            elif cmd == "PASSWORD_UNLOCK":
                # Unlock password display on LCD
                password_locked = False
                print("Password display unlocked")
                lcd_color(0, 255, 0)
                lcd_message("LCD Unlocked\nby admin")
                time.sleep(2)
            
                
    except:
        pass






#find motor number and activate it    
def activate_motor(motor_number):
    global access_count
    if motor_number == 1:
        motor = MOTOR_1
    elif motor_number == 2:
        motor = MOTOR_2
    else:
        print("Invalid motor number")
        return

    try:
        # Activate motor
        pca9685.set_pwm(motor, 2000)
        sleep(2)
        # Stop motor
        pca9685.set_pwm(motor, 1000)
        sleep(1)
        # Increase counter
        access_count += 1

        # Send updated count to admin
        send_count_to_admin()

    except Exception:
        print("Motor failed")



# MAIN program

print("HOTEL SYSTEM STARTING...")


# Send counter to admin
send_count_to_admin()

while True:
    try:
        check_adafruit_commands()
        temp()
        if system_enabled:
            lcd_color(0, 255, 0)
            lcd_message("System Ready  \nSystem: ON")
        else:
            lcd_color(255, 0, 0)
            lcd_message("System Standby \nSystem: OFF")
        
        # Keep motors in default
        pca9685.set_pwm(MOTOR_1, 1000)
        pca9685.set_pwm(MOTOR_2, 1000)
        
        if check_sensehat_reset():
            continue
        
        distance = ultrasonicRead(ultrasonic)
        time.sleep(0.5)
        
        if distance < 50:  
            print(f"Person detected starting system")
            time.sleep(0.5)
            
            if not system_enabled: # if system if disabled by adnin
                lcd_color(255, 0, 0)
                lcd_message("System disabled\nby admin")
                time.sleep(3)
                continue
            
            lcd_color(0, 255, 0)
            lcd_message("Welcome to  \nHotel System")
            time.sleep(2)
            
            if check_sensehat_reset():
                continue
            
            # generate new codes
            generate_random_codes()
            
            # clear old keypad data
            try:
                old = aio.receive(FEED_KEY)
                last_enter = old.value
                print(f"Clear old keypad value")
            except:
                last_enter = None
                print("No old values")
            
            # Room code 
            lcd_color(0, 128, 255)
            lcd_message("Please select \nyour room ")
            time.sleep(1)
            room_selected = False
            room = 0
            
            while not room_selected:
                check_adafruit_commands()
                
                if not system_enabled:
                    print("System disabled during room selection")
                    lcd_color(255, 0, 0)
                    lcd_message("System Disabled\nBy Admin")
                    time.sleep(2)
                    room = 0
                    break
                
                if check_sensehat_reset():
                    room_selected = True
                    room = 0
                    continue
                
                sensor_value = grovepi.analogRead(potentiometer)
                voltage = round((float)(sensor_value) * adc_ref / 1023, 2)
                degrees = round((voltage * full_angle) / grove_vcc, 2)
                
                if degrees < 150:
                    lcd_message("Select Room:   \nRoom 1")
                    grovepi.digitalWrite(led_red, 1)
                    grovepi.digitalWrite(led_blue, 0)
                    current_room = 1
                else:
                    lcd_message("Select Room: \nRoom 2")
                    grovepi.digitalWrite(led_red, 0)
                    grovepi.digitalWrite(led_blue, 1)
                    current_room = 2
                
                if digitalRead(button) == 1:
                    room = current_room
                    room_selected = True
                    grovepi.digitalWrite(led_blue, 0)
                    grovepi.digitalWrite(led_red, 0)
                    lcd_color(0, 255, 0)
                    lcd_message(f"Room {room}       \nConfirmed!")
                    for i in range(4):
                        grovepi.digitalWrite(led_blue, 1)
                        grovepi.digitalWrite(led_red, 1)
                        time.sleep(0.3)
                        grovepi.digitalWrite(led_red, 0)
                        grovepi.digitalWrite(led_blue, 1)
                        time.sleep(0.3)
                    
                    
                
                time.sleep(0.1)
            
            if room == 0:
                continue
            
            # to toggle room code
            if room == 1:
                active_code = code1
            else:
                active_code = code2
            
            # Check if password is locked or unlocked (affects LCD only)
            if password_locked:
                lcd_message(f"Room {room}\nAdmin has code")

            else:
                lcd_message(f"Room {room}\nCode:{active_code}")
            lcd_color(255, 255, 255)
            print("Waiting for keypad input...")
            code_correct = False
            
            while not code_correct:
                check_adafruit_commands()
                
                if not system_enabled:
                    lcd_color(255, 0, 0)
                    lcd_message("System Disabled\nBy Admin")
                    time.sleep(2)
                    room = 0
                    break
                
                if check_sensehat_reset():
                    code_correct = True
                    room = 0
                    continue
                
                try:
                    data = aio.receive(FEED_KEY)
                    enter = data.value
                except:
                    time.sleep(0.5)
                    continue
              
                if not enter or enter == last_enter:
                    time.sleep(0.5)
                    continue
                
                last_enter = enter
                print(f"Enter: {enter}")
                
                try:
                    enter_code = int(enter) #check if its number
                except:
                    
                    lcd_message("INVALID INPUT\nNumbers only")
                    time.sleep(2)
                    # Restore correct message based on lock state
                    if password_locked:
                        lcd_message(f"Room {room}\nAdmin has code")
                    else:
                        lcd_message(f"Room {room}\nCode: {active_code}")
                    lcd_color(255, 255, 255)
                    continue
                
                # CHECK CODE
                if enter_code == active_code:
                    print(f"ACCESS GRANTED for Room {room}")
                    
                    grovepi.digitalWrite(led_red, 0)
                    grovepi.digitalWrite(led_blue, 0)
                    if room == 1:
                        grovepi.digitalWrite(led_red, 1)
                    else:
                        grovepi.digitalWrite(led_blue, 1)
                    
                    lcd_color(0, 255, 0)
                    lcd_message(f"ACCESS GRANTED\nRoom {room}")
                    
                    for i in range(4):
                        grovepi.digitalWrite(led_red, 1)
                        grovepi.digitalWrite(led_blue, 1)
                        time.sleep(0.3)
                        grovepi.digitalWrite(led_red, 0)
                        grovepi.digitalWrite(led_blue, 1)
                        time.sleep(0.3)
                    
                    lcd_message("Thank you!    \nHave a nice stay")
                    time.sleep(2)
                    
                    # Ttrigger motor accordingly
                    activate_motor(room)
                    
                    code_correct = True
                
                else:
                    print("Wrong code!")
                    lcd_color(255, 0, 0)
                    lcd_message("INVALID CODE\nAccess Denied")
                    
                    for i in range(2):
                        grovepi.digitalWrite(led_red, 1)
                        grovepi.digitalWrite(buzzer, 1)
                        time.sleep(0.2)
                        grovepi.digitalWrite(led_red, 0)
                        grovepi.digitalWrite(buzzer, 0)
                        time.sleep(0.2)
                    
                    # Restore correct message based on lock state
                    if password_locked:
                        lcd_message(f"Room {room}\nAdmin has code")
                    else:
                        lcd_message(f"Room {room}\nCode: {active_code}")
                    lcd_color(255, 255, 255)
                
                time.sleep(0.5)
            
            if room == 0:
                continue
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("SYSTEM STOPPED")
        print("=" * 50)
        lcd_message("System\nStopped")
        lcd_color(255, 0, 0)
        grovepi.digitalWrite(led_blue, 0)
        grovepi.digitalWrite(led_red, 1)
        
        pca9685.set_pwm(MOTOR_1, 1000)
        pca9685.set_pwm(MOTOR_2, 1000)
        break
    
    except Exception as e:
        print(f"ERROR: {e}")
        lcd_color(255, 128, 0)
        lcd_message("System Error\nRetrying...")
        time.sleep(2)
