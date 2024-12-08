import RPi.GPIO as GPIO
import time

# Set up GPIO for Buzzer
buzzer_pin = 18  # GPIO pin connected to the Buzzer I/O
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
pwm = GPIO.PWM(buzzer_pin, 1000)  # Set initial frequency

# Function to play a beep sound
def beep(frequency, duration):
    pwm.ChangeFrequency(frequency)
    pwm.start(50)  # Start PWM with a 50% duty cycle
    time.sleep(duration)
    pwm.stop()

# Function to play dice roll sound for 4 seconds
def dice_roll_sound():
    print("Playing 'Dice Roll' sound...")
    # Alternate frequencies to simulate a dice rolling sound
    start_time = time.time()
    while time.time() - start_time < 4:  # Run sound for 4 seconds
        beep(1200, 0.1)  # Frequency 1200 Hz
        time.sleep(0.05)  # Short pause for rolling effect
        beep(1400, 0.1)  # Frequency 1400 Hz
        time.sleep(0.05)  # Short pause

# Function to play a win sound
def win_sound():
    for _ in range(3):
        beep(2000, 0.1)
        time.sleep(0.1)

# Function to play hit enemy sound
def hit_enemy():
    beep(1500, 0.3)

# Function to play a lose sound
def lose_sound():
    for _ in range(2):
        beep(500, 0.3)
        time.sleep(0.2)
