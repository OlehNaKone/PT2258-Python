import utime
from machine import I2C
from micropython import const


class PT2258:
    # Constants for volume, attenuation levels, and mute, clear registers.
    # These constants are defined using the const() function from micropython
    # to save memory on the microcontroller.
    __CLEAR_REGISTER: int = const(0xC0)
    __MASTER_VOLUME_10DB: int = const(0xD0)
    __MASTER_VOLUME_1DB: int = const(0xE0)
    __MUTE_REGISTER: int = const(0xF8)

    # Constants for channel registers 10dB
    __C1_10DB = const(0x80)
    __C2_10DB = const(0x40)
    __C3_10DB = const(0x00)
    __C4_10DB = const(0x20)
    __C5_10DB = const(0x60)
    __C6_10DB = const(0xA0)

    # Constants for channel registers 1dB
    __C1_1DB = const(0x90)
    __C2_1DB = const(0x50)
    __C3_1DB = const(0x10)
    __C4_1DB = const(0x30)
    __C5_1DB = const(0x70)
    __C6_1DB = const(0xB0)

    def __init__(self, port: I2C = None, address: int = 0x88) -> None:
        """
        Initialize the PT2258 6-channel volume controller.

        :param port: The I2C bus object connected to the PT2258.
        :type port: I2C
        :param address: The I2C address of the PT2258 (0x8C, 0x88, 0x84, or 0x80).
        :type address: int
        :raises ValueError: If the I2C object or address is not valid.
        :returns: None
        """
        # Check if the I2C object and address are valid.
        if port is None:
            raise ValueError("The 'port' I2C object is required to initialize PT2258.")
        if address not in [0x8C, 0x88, 0x84, 0x80]:
            raise ValueError(
                f"Invalid PT2258 device address {address}. It should be 0x8C, 0x88, 0x84, or 0x80."
            )

        # Store the I2C object and PT2258 address as class attributes.
        self.__I2C: I2C = port
        self.__PT2258_ADDR: int = const(address >> 1)

        # Define channel registers for both 10dB and 1dB settings.
        self.__CHANNEL_REGISTERS: tuple = (
            (self.__C1_10DB, self.__C1_1DB),  # channel 1 (10dB, 1dB)
            (self.__C2_10DB, self.__C2_1DB),  # channel 2 (10dB, 1dB)
            (self.__C3_10DB, self.__C3_1DB),  # channel 3 (10dB, 1dB)
            (self.__C4_10DB, self.__C4_1DB),  # channel 4 (10dB, 1dB)
            (self.__C5_10DB, self.__C5_1DB),  # channel 5 (10dB, 1dB)
            (self.__C6_10DB, self.__C6_1DB),  # channel 6 (10dB, 1dB)
        )

        # Initialize the last_ack variable to keep track of the last acknowledgment.
        self.__last_ack: int = 0

        # Initialize the PT2258 by calling the __initialize_pt2258() method.
        self.__initialize_pt2258()

    def __write_pt2258(self, write_data: int) -> int:
        """
        Write an instruction to the PT2258 via I2C.

        :param write_data: The instruction data to be written to PT2258.
        :type write_data: int
        :raises RuntimeError: If communication with PT2258 fails.
        :return: acknowledgment
        """
        try:
            # Try to write the instruction data to the PT2258 via I2C.
            ack: int = self.__I2C.writeto(self.__PT2258_ADDR, bytes([write_data]))
        except OSError as error:
            # Handle communication errors and raise a RuntimeError.
            if error.args[0] == 5:
                raise RuntimeError(
                    "Communication error with the PT2258 during the operation."
                )
            else:
                raise RuntimeError(
                    f"Communication error with the PT2258. Error message: {error}"
                )
        return ack

    def __initialize_pt2258(self) -> None:
        """
        Initialize the PT2258 6-channel volume controller IC.

        After power is turned on, PT2258 needs to wait for at least 200ms to ensure stability.
        If the waiting time period is less than 200ms, I2C control may fail.

        In order to ensure exact operation under any operating voltage,
        it is recommended to clear the register "C0H" as the first step of initialization.

        :raises OSError: If the PT2258 device is not present on the I2C bus.
        :return: None
        """
        # Wait for at least 300ms for stability after power-on.
        utime.sleep_ms(300)

        # Check if the PT2258 device is present on the I2C bus.
        if self.__PT2258_ADDR not in self.__I2C.scan():
            raise OSError("PT2258 not found on the I2C bus.")

        # Clear the specified register to initialize the PT2258.
        self.__write_pt2258(self.__CLEAR_REGISTER)

    def master_volume(self, volume: int = 0) -> int:
        """
        Set the master volume.

        :param volume: The desired master volume level (0 to 79).
        :type volume: int
        :raises ValueError: If the provided volume is outside the range 0 to 79.
        :return: int
        """
        # Validate the volume input.
        if not 0 <= volume <= 79:
            raise ValueError("The master volume should be within the range of 0 to 79.")

        # Calculate attenuation values for 10dB and 1dB settings.
        att_10db, att_1db = divmod(79 - volume, 10)

        # Send attenuation settings to the PT2258, first 10dB and then 1dB.
        self.__last_ack: int = self.__write_pt2258(
            self.__MASTER_VOLUME_10DB | att_10db,
        )
        if self.__last_ack:
            self.__last_ack: int = self.__write_pt2258(
                self.__MASTER_VOLUME_1DB | att_1db
            )
        return self.__last_ack

    def channel_volume(self, channel: int, volume: int = 0) -> int:
        """
        Set the volume level for a specific channel.

        :param channel: The index of the channel (0 to 5).
        :type channel: int
        :param volume: The desired volume level for the channel (0 to 79).
        :type volume: int
        :raises ValueError: If the provided channel or volume is outside the valid range.
        :return: int
        """
        # Validate the channel and volume inputs.
        if not 0 <= volume <= 79:
            raise ValueError("The volume should be within the range of 0 to 79.")
        if not 0 <= channel <= 5:
            raise ValueError(
                "Invalid channel index. Channels should be within the range of 0 to 5."
            )

        # Get the 10dB and 1dB channel registers for the specified channel.
        channel_10db, channel_1db = self.__CHANNEL_REGISTERS[channel]

        # Calculate attenuation values for 10dB and 1dB settings.
        att_10db, att_1db = divmod(79 - volume, 10)

        # Send attenuation settings to the PT2258, first 10dB and then 1dB.
        self.__last_ack: int = self.__write_pt2258(channel_10db | att_10db)
        if self.__last_ack:
            self.__last_ack: int = self.__write_pt2258(channel_1db | att_1db)
        return self.__last_ack

    def mute(self, status: bool = False) -> int:
        """
        Enable or disable the mute functionality.

        :param status: If True, mute is enabled. If False, mute is disabled.
        :type status: bool
        :raises ValueError: If the provided status is not a boolean value.
        :return: int
        """
        # Validate the mute status input.
        if not isinstance(status, bool):
            raise ValueError(
                "Invalid mute status value. It should be a boolean (True or False)."
            )

        # Send the mute status to the PT2258 and store the acknowledgment.
        self.__last_ack: int = self.__write_pt2258(self.__MUTE_REGISTER | status)
        return self.__last_ack
