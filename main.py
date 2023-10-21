import utime
from machine import Pin, I2C

from PT2258 import PT2258

if __name__ == "__main__":
    # Create an I2C object for communication with PT2258
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

    # Create an instance of the PT2258 class
    pt2258 = PT2258(port=i2c, address=0x88)

    print("Hello, world!")
    utime.sleep(2)
    print("PT2258 test script starting...")
    utime.sleep(5)

    # Set all channels' volume to 0
    for channel in range(6):
        pt2258.channel_volume(channel, 0)
    pt2258.master_volume(0)

    while True:
        # The following loops simulate volume changes, similar to a rotary encoder or potentiometer.

        # Increase master volume.
        for volume in range(80):
            print(
                f"Master volume: {volume} Volume is at maximum"
                if volume == 79
                else f"Master volume: {volume}dB"
            )
            pt2258.master_volume(volume)
            utime.sleep(0.5)  # Wait for half a second before the next volume change.

        utime.sleep(10)
        # Decrease master volume
        for volume in range(80):
            print(
                f"Master volume: {volume} Volume is at maximum "
                if volume == 79
                else f"Master volume: -{volume}dB"
            )
            pt2258.master_volume(79 - volume)
            utime.sleep(0.5)  # Wait for half a second before the next volume change

        # Set volume to maximum
        print("Volume at maximum")
        pt2258.master_volume(79)
        utime.sleep(10)

        # Mute and UnMute
        print("Muted. Please wait...")
        pt2258.mute(True)
        utime.sleep(5)
        print("UnMuted")
        pt2258.mute(False)
        utime.sleep(10)

# This code just simulating how to use the class methods, Please refer the README.md/Usage/.
