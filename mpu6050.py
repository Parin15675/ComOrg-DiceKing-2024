import smbus
import time

class mpu6050:
    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)  # Use SMBus 1 on Raspberry Pi
        self.setup_sensor()

    def setup_sensor(self):
        # Configure the sensor
        # Set the power management register to 0 to activate the sensor
        self.bus.write_byte_data(self.address, 0x6B, 0)
        print(f"MPU6050 initialized at address {hex(self.address)}")

    def read_i2c_word(self, register):
        # Read data from the register
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) + low
        # Check the sign bit and adjust
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def get_accel_data(self):
        # Read data from the accelerometer
        x = self.read_i2c_word(0x3B)
        y = self.read_i2c_word(0x3D)
        z = self.read_i2c_word(0x3F)
        return {
            'x': x / 16384.0,
            'y': y / 16384.0,
            'z': z / 16384.0
        }

    def get_gyro_data(self):
        # Read data from the gyroscope
        x = self.read_i2c_word(0x43)
        y = self.read_i2c_word(0x45)
        z = self.read_i2c_word(0x47)
        return {
            'x': x / 131.0,
            'y': y / 131.0,
            'z': z / 131.0
        }
        
        
# Initialize the I2C bus
bus = smbus.SMBus(1)
MPU6050_ADDRESS = 0x68

# Register the MPU6050
bus.write_byte_data(MPU6050_ADDRESS, 0x6B, 0)

# Function to read acceleration data from MPU6050
def read_accel():
    raw_x = bus.read_byte_data(MPU6050_ADDRESS, 0x3B) << 8 | bus.read_byte_data(MPU6050_ADDRESS, 0x3C)
    raw_y = bus.read_byte_data(MPU6050_ADDRESS, 0x3D) << 8 | bus.read_byte_data(MPU6050_ADDRESS, 0x3E)
    raw_z = bus.read_byte_data(MPU6050_ADDRESS, 0x3F) << 8 | bus.read_byte_data(MPU6050_ADDRESS, 0x40)
    
    # Convert to signed values
    accel_x = (raw_x if raw_x < 32768 else raw_x - 65536)
    accel_y = (raw_y if raw_y < 32768 else raw_y - 65536)
    accel_z = (raw_z if raw_z < 32768 else raw_z - 65536)
    
    return accel_x, accel_y, accel_z
    
# Function to check for a shake event
def is_shaken(threshold=70000, duration=1):
    accel_x, accel_y, accel_z = read_accel()
    magnitude = abs(accel_x) + abs(accel_y) + abs(accel_z)
    
    if magnitude > threshold:
        print(f"Shake detected with magnitude: {magnitude}")
        return True
    return False
