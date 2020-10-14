from time import sleep
from pymata4 import pymata4
from typing import (
    AnyStr
)


class LiquidCrystal_I2C:
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    LCD_BACKLIGHT = 0x08
    LCD_NOBACKLIGHT = 0x00

    ENABLE_BIT = 0B00000100  # Enable bit
    READ_WRITE_BIT = 0B00000010  # Read/Write bit
    REGISTER_SELECT_BIT = 0B00000001  # Register select bit

    _backlight_value: int = LCD_NOBACKLIGHT
    _display_function: int = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
    _numlines: int = None
    _display_control: int = None
    _display_mode: int = None
    _oled: bool = True

    def write(self, value: int):
        self.send(value, self.REGISTER_SELECT_BIT)

    def __init__(self, address: int, column: int, row: int, board: pymata4.Pymata4, dotsize: int = 1) -> None:
        self.address: int = address
        self.column: int = column
        self.row: int = row
        if not isinstance(board, pymata4.Pymata4):
            raise AttributeError("argument board not from pymata4.Pymata4")
        else:
            self.board: pymata4.Pymata4 = board

        self.begin(self.column, self.row, dotsize=dotsize)

    def begin(self, column: int, lines: int, dotsize: int = LCD_5x8DOTS) -> None:
        self.board.set_pin_mode_i2c()

        if lines >= 1:
            self._display_function = self._display_function | self.LCD_2LINE

        self._numlines = lines

        if dotsize != 0 and lines == 1:
            self._display_function = self._display_function | self.LCD_5x10DOTS

        sleep(0.05)

        self.expander_write(self._backlight_value)
        sleep(1)

        self.write_4_bits(0x03 << 0x4)
        sleep(0.0045)

        self.write_4_bits(0x03 << 0x4)
        sleep(0.0045)

        self.write_4_bits(0x03 << 0x4)
        sleep(0.00015)

        self.write_4_bits(0x02 << 0x4)

        self.command(self.LCD_FUNCTIONSET | self._display_function)

        self._display_control = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.enable_display()

        self.clear()

        self._display_mode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.command(self.LCD_ENTRYMODESET | self._display_mode)

        self.home()

    def clear(self):
        self.command(self.LCD_CLEARDISPLAY)
        sleep(0.002)
        if self._oled:
            self.set_cursor(0, 0)

    def home(self) -> None:
        self.command(self.LCD_RETURNHOME)
        sleep(0.002)

    def set_cursor(self, column: int, row: int) -> None:
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row > self._numlines:
            row = self._numlines - 1
        self.command(self.LCD_SETDDRAMADDR | (column + row_offsets[row]))

    def disable_display(self) -> None:
        self._display_control = self._display_control & ~self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYON | self._display_control)

    def enable_display(self) -> None:
        self._display_control = self._display_control | self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL | self._display_control)

    def disable_cursor(self) -> None:
        self._display_control = self._display_control & ~self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL | self._display_control)

    def enable_cursor(self) -> None:
        self._display_control = self._display_control | self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL | self._display_control)

    def disable_blink(self) -> None:
        self._display_control = self._display_control & ~self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL | self._display_control)

    def enable_blink(self) -> None:
        self._display_control = self._display_control | self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL | self._display_control)

    def scroll_display_left(self) -> None:
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def scroll_display_right(self) -> None:
        self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def left_to_right(self) -> None:
        self._display_mode = self._display_mode | self.LCD_ENTRYLEFT
        self.command(self.LCD_ENTRYMODESET | self._display_mode)

    def right_to_left(self) -> None:
        self._display_mode = self._display_mode & ~self.LCD_ENTRYLEFT
        self.command(self.LCD_ENTRYMODESET | self._display_mode)

    def enable_auto_scroll(self) -> None:
        self._display_mode = self._display_mode | self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_ENTRYMODESET | self._display_mode)

    def disable_auto_scroll(self) -> None:
        self._display_mode = self._display_mode & ~self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_ENTRYMODESET | self._display_mode)

    def disable_backlight(self) -> None:
        self._backlight_value = self.LCD_NOBACKLIGHT
        self.expander_write(0)

    def enable_backlight(self) -> None:
        self._backlight_value = self.LCD_BACKLIGHT
        self.expander_write(0)

    def command(self, value) -> None:
        self.send(value, 0)

    def send(self, value: int, mode: int) -> None:
        high_nibble: int = value & 0xf0
        low_nibble: int = (value << 4) & 0xf0
        self.write_4_bits(high_nibble | mode)
        self.write_4_bits(low_nibble | mode)

    def write_4_bits(self, value: int) -> None:
        self.expander_write(value)
        self.pulse_enable(value)

    def expander_write(self, data: int) -> None:
        self.board.i2c_write(self.address, [data, self._backlight_value])

    def pulse_enable(self, data: int) -> None:
        self.expander_write(data | self.ENABLE_BIT)
        sleep(0.000001)

        self.expander_write(data & ~self.ENABLE_BIT)
        sleep(0.00005)

    def print(self, string: AnyStr) -> None:
        for character in string:
            self.write(ord(character))
            sleep(0.000001)
        else:
            sleep(0.00005)


Board = pymata4.Pymata4("/dev/ttyACM0")
LCD = LiquidCrystal_I2C(0x27, 0, 1, Board)
LCD.enable_backlight()
LCD.print("Hello, Worlds!")