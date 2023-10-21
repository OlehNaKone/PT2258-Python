# PT2258 6-Channel Electronic Volume Controller IC

This class provides a MicroPython implementation for controlling the PT2258 6-Channel Electronic Volume Controller IC
using I2C communication.

## Table of Contents

- [Overview](#overview)
- [Usage](#usage)
    - [Finding Device Address](#finding-device-address)
        - [PT2258 address code](#pt2258-address-code)
        - [Find PT2258](#find-pt2258)
    - [Example Usage](#example-usage)
    - [Test Script](#test-script)
    - [Multy device configure](#multy-device-configure)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
    - [Class API Reference](#class-api-reference)
- [Contributions](#contributions)
- [Requirements](#requirements)
- [Credits](#credits)
- [License](#license)

## Overview

Overview

The `PT2258` class provides comprehensive control over the `PT2258` IC, a versatile 6-channel volume controller. With
this
class, you can effortlessly manage various audio parameters, including:

- `Master Volume Control:` Adjust the master volume level dynamically to fine-tune your audio output.
- `Individual Channel Volume:` Customize the volume levels for each of the six available channels, allowing precise
  audio
  channel management.
- `Mute Functionality:` Conveniently enable or disable the mute function, ensuring flexible audio control.

This class empowers you to integrate the `PT2258` IC seamlessly into your projects, opening up a world of possibilities
for audio customization and optimization. Whether you're building audio equipment, home automation systems, or any other
project requiring advanced audio control, the `PT2258` class simplifies the process while delivering exceptional audio
quality and flexibility.

## Usage

To use the `PT2258` class, follow these steps:

1. `Initialize an I2C bus object connected to the PT2258.`
2. `Configure the communication frequency to 100kHz.`
3. `Provide the I2C address of the PT2258 (0x8C, 0x88, 0x84, or 0x80).`

### Finding Device Address

The following instructions explain how to configure and obtain a device address.

### PT2258 address code

PT2258 Address Code depends on the state of CODE1 (Pin No.17) and CODE2 (Pin No.4).
If CODE1 or CODE2 is connected to Vcc, then CODE1 or CODE2 is set to “1”. If CODE1 or CODE2 is connected to the
Ground, it is set to “0”. Please refer to the information below:

| Condition | CODE1 | CODE2 | PT2258 Address Code |
|-----------|-------|-------|---------------------|
| 1         | 1     | 1     | 8CH                 |
| 2         | 1     | 0     | 88H                 |
| 3         | 0     | 0     | 84H                 |
| 4         | 0     | 0     | 80H                 |

### Find PT2258

If you struggle to get device address.
Use this code to find I2C device addresses in hexadecimal format and raise an error if not found:

```python
from machine import I2C, Pin

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
valid_addresses = [0x8C, 0x88, 0x84, 0x80]

address = ', '.join(hex(addr) for addr in valid_addresses if addr in i2c.scan())
print(f"PT2258 found devices at addresses: {address}. :)" if address else "PT2258 not found on the bus. :(")
```

### Example Usage

Certainly! It demonstrates how to use the class methods to control the audio settings.If you have any specific concerns
or modifications you'd like to make to this code, please feel free to specify them.

```python
import utime
from machine import Pin, I2C

from PT2258 import PT2258

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

pt2258 = PT2258(port=i2c, address=0x88)


def main() -> None:
    # set all channel volume in to o.
    for channel in range(6):
        pt2258.channel_volume(channel, 0)
    pt2258.master_volume(0)
    while True:
        for volume in range(80):
            print('Volume is at maximum' if volume == 79 else f'Master volume: {volume}dB')
            pt2258.master_volume(volume)
            utime.sleep(0.5)  # Every half second the master volume raises up
        utime.sleep(10)  # The program back to loop.


if __name__ == '__main__':
    main()

```

### Test Script

testing all the methods' functionality.

```python
import utime
from PT2258 import PT2258
from machine import Pin, I2C

# Create an I2C object for communication with PT2258
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Create an instance of the PT2258 class
pt2258 = PT2258(port=i2c, address=0x88)


def main() -> None:
    """
    Main function for testing the PT2258 volume controller.
 
    This function initializes the PT2258, sets all channels to zero volume, and then gradually increases and decreases
    the master volume to simulate a volume control action.
 
    :return: None
    """

    print('Hello, world!')
    utime.sleep(2)
    print('PT2258 test script starting...')
    utime.sleep(5)

    # Set all channels to 0 volume
    for channel in range(6):
        pt2258.channel_volume(channel, 0)
    pt2258.master_volume(0)

    while True:
        # The following loops simulate volume changes, similar to a rotary encoder or potentiometer.

        # Increase volume
        for volume in range(80):
            print('Volume is at maximum' if volume == 79 else f'Master volume: {volume}dB')
            pt2258.master_volume(volume)
            utime.sleep(0.5)  # Wait for half a second before the next volume change

        # Decrease volume
        for volume in range(80):
            print('Volume is at maximum' if volume == 79 else f'Master volume: -{volume}dB')
            pt2258.master_volume(79 - volume)
            utime.sleep(0.5)  # Wait for half a second before the next volume change

        # Set volume to maximum
        print('Volume at maximum')
        pt2258.master_volume(79)
        utime.sleep(10)

        # Mute and UnMute
        print('Muted. Please wait...')
        pt2258.mute(True)
        utime.sleep(5)
        print('UnMuted')
        pt2258.mute(False)
        utime.sleep(10)


if __name__ == '__main__':
    main()
```

Feel free to explore and adapt these examples to suit your specific project requirements.

### MULTY DEVICE CONFIGURE

**Note:** The code initializes multiple PT2258 ICs with different I2C addresses.

```python
from machine import Pin, I2C
from PT2258 import PT2258

# Create an I2C object for communication with PT2258
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Create an instance of the PT2258 class for the first PT2258 IC
pt2258_1 = PT2258(port=i2c, address=0x80)  # Initialize the PT2258 IC with address 0x80

# Create instances for the other three PT2258 ICs with different addresses
pt2258_2 = PT2258(port=i2c, address=0x84)  # Initialize the PT2258 IC with address 0x84
pt2258_3 = PT2258(port=i2c, address=0x88)  # Initialize the PT2258 IC with address 0x88
pt2258_4 = PT2258(port=i2c, address=0x8C)  # Initialize the PT2258 IC with address 0x8C

# Set the master volume for the 1st PT2258 to 10 (Range typically 0-79)
pt2258_1.master_volume(10)

# Set the master volume for the 2nd PT2258 to 40 (Range typically 0-79)
pt2258_2.master_volume(40)

# Set the volume for the 1st channel of the 3rd PT2258 to 15 (Range typically 0-79)
pt2258_3.channel_volume(channel=1, volume=15)

# Set the volume for the 4th channel of the 4th PT2258 to 20 (Range typically 0-79)
pt2258_4.channel_volume(channel=4, volume=20)

# Mute the 1st PT2258 (status=True mutes, status=False UnMutes)
pt2258_1.mute(status=True)

# Mute the 2nd PT2258 (status=True mutes, status=False UnMutes)
pt2258_2.mute(status=True)
```

**It uses four different addresses to run four different PT2258 in single I2C bus.**

# Documentation

For comprehensive details about the `PT2258` functionality and usage, please refer to the
official [PT2258 documentation](https://www.princeton.com.tw/Portals/0/activeforums_Attach/PT2258-s.pdf?ver=_PKEbk4RdtE4NR8jQD-U9g%3d%3d).

The class documentation offers in-depth explanations, usage examples, and detailed parameter information for each
method.

# Getting Started

If you're new to the `PT2258` 6-Channel Electronic Volume Controller IC and its usage with the provided MicroPython
code,
here's how to start:

Clone or download this [repository](https://github.com/zerovijay/PT2258) to your local machine.
Review the class documentation to understand available methods and usage. Utilize the `__doc__` method
or `help()` to explore class details.
Follow the example usage provided in the Usage section of this [README.md](README.md)
file to integrate the PT2258 class into your project.
If you have any suggestions or find issues, feel free to contribute by creating issues or pull requests on
the [repository](https://github.com/zerovijay/PT2258).

### Class API Reference

The class methods are documented in the `PT2258` class documentation. It includes the following methods:

- `__init__(self, port: I2C = None, address: int = None) -> None`: Initialize the PT2258 instance.
- `master_volume(self, volume: int) -> None`: Set the master volume level.
- `channel_volume(self, channel: int, volume: int) -> None`: Set the specific channel volume.
- `mute(self, status: bool = False) -> None`: Enable or disable the mute functionality.

# Contributions

If you find any issues or have suggestions for improvements, feel free to contribute by creating issues or pull requests
on the [repository](https://github.com/zerovijay/PT2258).

# Requirements

- [Python](https://www.python.org)
- [MicroPython](https://micropython.org)
- [MicroPython Compatible Boards](https://micropython.org/download)
- [PT2258 6-Channel Electronic Volume Controller IC](https://www.princeton.com.tw/Portals/0/activeforums_Attach/PT2258-s.pdf?ver=_PKEbk4RdtE4NR8jQD-U9g%3d%3d)

# Credits

This code was created by [@zerovijay](https://github.com/zerovijay). We appreciate your contributions to enhance this
project!

# License

This project is licensed under the [MIT License](LICENSE.md).
