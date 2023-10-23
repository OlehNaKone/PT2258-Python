import utime
from machine import Pin, I2C

from PT2258 import PT2258

"""
This code explains how to use the class methods and how to use the acknowledgments bit from the slave (PT2258).
This is overkill but whynot?
"""

if __name__ == "__main__":
    # Create an I2C object for communication with PT2258
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

    # Create an instance of the PT2258 class
    pt2258 = PT2258(port=i2c, address=0x88)

    # This variable is used to track the last acknowledgments from PT2258.
    # This helps to minimize data bottleneck, I2C overhead.
    last_ack: int = 0

    print("Hello, world!")
    utime.sleep(2)
    print("PT2258 test script starting...")
    utime.sleep(5)

    # Set all channels' volume to 0
    for channel in range(6):
        last_ack = pt2258.channel_volume(channel, 0)
        # We need to wait for acknowledgments.
        while last_ack:
            pass
    last_ack = pt2258.master_volume(0)
    while last_ack:
        pass

    while True:
        # The following loops simulate volume changes, similar to a rotary encoder or potentiometer.

        # Increase master volume.
        for volume in range(80):
            last_ack = pt2258.master_volume(volume)
            if last_ack:
                print(
                    f"Master volume: {volume} Volume is at maximum"
                    if volume == 79
                    else f"Master volume: {volume}dB"
                )

            # We need to wait for next acknowledgments from PT2258.
            while last_ack:
                pass
            utime.sleep(0.5)  # Wait for half a second before the next volume change.
        utime.sleep(10)

        # Decrease master volume
        for volume in range(80):
            last_ack = pt2258.master_volume(79 - volume)
            if last_ack:
                print(
                    f"Master volume: {volume} Volume is at maximum"
                    if volume == 79
                    else f"Master volume: -{volume}dB"
                )

            # We need to wait for next acknowledgments from PT2258.
            while last_ack:
                pass
            utime.sleep(0.5)  # Wait for half a second before the next volume change

        # Set volume to maximum
        last_ack = pt2258.master_volume(79)
        if last_ack:
            print("Volume at maximum")
        utime.sleep(10)

        # Mute and UnMute
        last_ack = pt2258.mute(True)
        if last_ack:
            print("Muted. Please wait...")
        utime.sleep(5)

        last_ack = pt2258.mute(False)
        if last_ack:
            print("UnMuted")
        utime.sleep(10)

# This code is just simulating how to use the class methods. Please refer to the README.md/Usage/.
