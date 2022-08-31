# circuitpython_dfrobot_gravity_drf0627_dual_uart: Copyright (c) 2022 Graham Beland
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_dfrobot_gravity_drf0627_dual_uart`
================================================================================
* Author(s): Graham Beland, Sept. 2022
Implementation Notes
--------------------
**Hardware:**
**Software and Dependencies:**
* Adafruit CircuitPython <https://github.com/adafruit/circuitpython>
* Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>
* Adafruit CircuitPython firmware for the supported boards:
* https://circuitpython.org/downloads
* Adafruit's Bus Device library:
* https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

 @file DFRobot_IIC_Serial.py
 @brief Define the basic structure of class DFRobot_IIC_Serial
 @n This is a library for IIC to UART module, the maximum rate is 1Mbps
 @n The band rate, word length, and check format
 @ of every sub UART can be set independently
 @n The module can provide at most 2Mbps communication rate
 @n Each sub UART is able to receive/transmit independent 256 bytes FIFO hardware cache
 @n Users can configure FIFO interrupt by programming.

 @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 @license     The MIT License (MIT)
 @author [Arya](xue.peng@dfrobot.com)
 @version  V1.1
 @date  2021-05-07
 @https://github.com/DFRobot/DFRobot_IIC_Serial
"""
# imports

__version__ = "0.0.0-auto.0"
__repo__ = (
    "https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart.git"
)


import time
import array as arr

class DFRobot_IIC_Serial:
    """DFRobot_IIC_Serial"""
    # Global control register, control sub UART clock
    REG_WK2132_GENA = 0x00
    # Global sub UART reset register, reset a sub UART independently through software
    REG_WK2132_GRST = 0x01
    # Global main UART control register, and will be used only when the main UART
    # is selected as UART, no need to be set here.
    REG_WK2132_GMUT = 0x02
    # Global interrupt register, control sub UART total interrupt.
    REG_WK2132_GIER = 0x10
    # Global interrupt flag register, only-read register: indicate
    # if there is a interrupt occuring on a sub UART.
    REG_WK2132_GIFR = 0x11
    # sub UART page control register
    REG_WK2132_SPAGE = 0x03
    # Sub UART control register
    REG_WK2132_SCR = 0x04
    # Sub UART configuration register
    REG_WK2132_LCR = 0x05
    # Sub UART FIFO control register
    REG_WK2132_FCR = 0x06
    # Sub UART interrupt enable register
    REG_WK2132_SIER = 0x07
    # Sub UART interrupt flag register
    REG_WK2132_SIFR = 0x08
    # Sub UART transmit FIFO register, OR register
    REG_WK2132_TFCNT = 0x09
    # Sub UART transmit FIFO register, OR register
    REG_WK2132_RFCNT = 0x0A
    # Sub UART FIFO register, OR register
    REG_WK2132_FSR = 0x0B
    # Sub UART receive register, OR register
    REG_WK2132_LSR = 0x0C
    # Sub UART FIFO data register
    REG_WK2132_FDAT = 0x0D
    # Sub UART band rate configuration register high byte
    REG_WK2132_BAUD1 = 0x04
    # Sub UART band rate configuration register low byte
    REG_WK2132_BAUD0 = 0x05
    # Sub UART band rate configuration register decimal part
    REG_WK2132_PRES = 0x06
    # Sub UART receive FIFO interrupt trigger configuration register
    REG_WK2132_RFTL = 0x07
    # Sub UART transmit FIFO interrupt trigger configuration register
    REG_WK2132_TFTL = 0x08
    # Sub UART channel1
    SUBUART_CHANNEL_1 = 0x00
    # Sub UART channel2
    SUBUART_CHANNEL_2 = 0x01
    # All sub channels
    SUBUART_CHANNEL_ALL = 0x11
    # The 4th and 3rd bits of IIC address are fixed, value 1 and 0 respectively
    IIC_ADDR_FIXED = 0x10

    SERIAL_RX_BUFFER_SIZE = 32
    IIC_BUFFER_SIZE = 64

    ERR_OK = 0
    ERR_REGDATA = -1
    ERR_READ = -2
    FOSC = 14745600  # External cystal frequency 14.7456MHz
    OBJECT_REGISTER = 0x00  # Register object
    OBJECT_FIFO = 0x01  # FIFO buffer object

    """
    Data format:
    N for no parity,
    Z for 0 parity,
    O for Odd parity,
    E for Even parity,
    F for 1 parity.
    8 represents the number of data bit, 1 or 2 for the number of stop bit.
    """
    IIC_Serial_8N1 = 0x00
    IIC_Serial_8N2 = 0x01
    IIC_Serial_8Z1 = 0x08
    IIC_Serial_8Z2 = 0x09
    IIC_Serial_8O1 = 0x0A
    IIC_Serial_8O2 = 0x0B
    IIC_Serial_8E1 = 0x0C
    IIC_Serial_8E2 = 0x0D
    IIC_Serial_8F1 = 0x0E
    IIC_Serial_8F2 = 0x0F

    eNormalMode = 0
    eNormal = 0

    _rx_buffer = [0] * SERIAL_RX_BUFFER_SIZE
    """
    # LCR description of WK2132 sub UART configuration register:
    # -------------------------------------------------------------------------
    # |   b7   |   b6   |   b5   |   b4   |   b3   |   b2   |   b1   |   b0   |
    # -------------------------------------------------------------------------
    # |        RSV      |  BREAK |  IREN  |  PAEN  |      PAM        |  STPL  |
    # -------------------------------------------------------------------------
    """
    # Sub UART data format:
    # PAEN sub UART check enable bit,
    # 1-with parity bit(9-bits data),
    # 0-no parity bit (8-bits data) PAM sub UART check mode selection bit,
    # take effect when PAEN bit is 1,
    # 00-0 parity(default),
    # 01-Odd parity
    # 10-Even parity,
    # 11-1 parity,
    # STPL sub UART stop bit length, 0-1bit, 1-2bits, etc.
    sLcrReg_format = 0x0F
    # Sub UART IR enable bit, 0-normal mode, 1-IR mode
    sLcrReg_irEn = 1 << 4
    # Sub UART Line-Break output control bit, 0-output normally,
    # 1-Line-Break output (TX force output 0)
    sLcrReg_lBreak = 1 << 5
    # Reserved bit
    sLcrReg_rsv = 1 << 6

    sIICAddr_type = 1 << 0
    sIICAddr_uart = 1 << 1
    sIICAddr_addrPre = 0x1F << 3
    # Sub UART transmit TX busy flag bit,
    # 0-sub UART transmit TX null,
    # 1-sub UART transmit TX busy
    sFsrReg_tBusy = 1 << 0
    # Sub UART transmit TX full flag bit,
    # 0-sub UART transmit FIFO not full,
    # 1-sub UART transmit FIFO full
    sFsrReg_tFull = 1 << 1
    # Sub UART transmit FIFO null flag,
    # 0-sub UART transmit FIFO null,
    # 1-sub UART transmit FIFO not null
    sFsrReg_tDat = 1 << 2
    # Sub UART receive FIFO null flag,
    # 0-sub UART receive FIFO null,
    # 1-sub UART receive FIFO not null
    sFsrReg_rDat = 1 << 3
    # Sub UART receive FIFO data check error flag bit, 0- no PE error, 1-PE error
    sFsrReg_rFpe = 1 << 4
    # Sub UART receive FIFO data frame error flag bit,
    # 0-no FE error, 1-FE error
    sFsrReg_rFfe = 1 << 5
    # Sub UART receive FIFO data Line-break error,
    # 0-no Line-Break error, 1-Line-Break error
    sFsrReg_rFbi = 1 << 6
    # Sub UART receive FIFO data overflow error flag bit,
    # 0-no OE error, 1-OE error
    sFsrReg_rFoe = 1 << 7

    STA_OK = 0x00
    STA_ERR = 0x01
    STA_ERR_DEVICE_NOT_DETECTED = 0x02
    STA_ERR_SOFT_VERSION = 0x03
    STA_ERR_PARAMETER = 0x04

    # last operate status, users can use this variable
    # to determine the result of a function call.
    last_operate_status = STA_OK

    def __init__(self, i2c, sub_uart_channel, IA1=1, IA0=1):
        """!
        @brief Constructor
        @param sub_uart_channel sub UART channel,
        @n WK2132 has two sub UARTs: SUBUART_CHANNEL_1 or SUBUART_CHANNEL_2
        @param IA1:  corresponds with IA1 Level(0 or 1)
        @n of DIP switch on the module, and is used for configuring
        @n the IIC address of the 6th bit value(default: 1).
        @param  IA0:  corresponds with IA0 Level(0 or 1)
        @n of DIP switch on the module, and is used for configuring
        @n IIC address of the 5th bit value(default: 1).
        @n IIC address configuration:
        @n 7   6   5   4   3   2   1   0
        @n 0  IA1 IA0  1   0  C1  C0  0/1
        @n IIC address only has 7 bits, while there are 8 bits
        @n for one byte, so the extra one bit will be filled as 0.
        @n The 6th bit corresponds with IA1 Level of DIP switch,
        @n can be configured manually.
        @n The 5th bit corresponds with IA0 Level of DIP switch,
        @n can be configured manually.
        @n The 4th and 3rd bits are fixed, value 1 and 0 respectively.
        @n The values of the 2nd and 1st bits are the sub UART channels,
        00 for sub UART 1, 01 for sub UART 2.
        @n The 0 bit represents the operation object: 0 for register, 1 for FIFO cache.
        """
        self._addr = (IA1 << 6) | (IA0 << 5) | self.IIC_ADDR_FIXED
        self._sub_serial_channel = sub_uart_channel
        self._rx_buffer_head = 0
        self._rx_buffer_tail = 0
        self._i2c = i2c

    def begin(self, baud, theformat=IIC_Serial_8N1):
        """!
        @brief Init function, set sub UART band rate, data format
        @param baud: baud rate, it support: 9600, 57600, 115200, 2400, 4800, 7200,
        @n     14400, 19200, 28800,38400, 76800, 153600, 230400, 460800, 307200, 921600
        @param format: Data format, it support:
        @n     IIC_SERIAL_8N1, IIC_SERIAL_8N2, IIC_SERIAL_8Z1,IIC_SERIAL_8Z2
        @n     IIC_SERIAL_8O1, IIC_SERIAL_8O2, IIC_SERIAL_8E1, IIC_SERIAL_8E2
        @n     IIC_SERIAL_8F1, IIC_SERIAL_8F2
        @return Return 0 if it sucess, otherwise return non-zero
        """
        return self._begin(baud, theformat, self.eNormalMode, self.eNormal)

    def end(self):
        """!
        @brief Release sub UART to clean up all registers in
        @n Sub UART. Call function begin() again to make it work.
        """
        self._sub_serial_global_reg_enable(self._sub_serial_channel, 1)

    def printf(self, *args, **kargs):
        """!
        @brief The Prints the values to a stream, usage is the same as print function.
        @param args
        @param kargs
        @n sep: string inserted between values, default a space.
        @n end: string appended after the last value, default a newline.
        """
        sep = kargs.pop("sep", " ")
        end = kargs.pop("end", "\n")
        if kargs:
            raise TypeError("extra keywords:%s" % kargs)
        first = True
        output = ""
        for arg in args:
            output += ("" if first else sep) + str(arg)
            first = False
            # print(arg)
        output += end
        self.write(output)

    def available(self):
        """!
        @brief Get the number of bytes in receive buffer,
        @n it should be the total number of bytes in FIFO
        @n receive buffer(256B) and self-defined _rx_buffer(31B).
        @return Return the number of bytes in receive buffer
        """
        thebs = self._read_bytes(self.REG_WK2132_RFCNT, 1)
        index = 0
        if len(thebs) != 1:
            print("READ BYTE SIZE ERROR!")
            return 0
        index = int(thebs[0])
        if index == 0:
            fsr = self._read_fifo_state_reg()
            if (fsr & self.sFsrReg_rDat) > 0:
                index = 256
        return (
            index
            + (self.SERIAL_RX_BUFFER_SIZE + self._rx_buffer_head - self._rx_buffer_tail)
            % self.SERIAL_RX_BUFFER_SIZE
        )

    def peek(self):
        """!
        @brief Return the data of 1 byte without deleting the data in the receive buffer
        @return Return the readings
        """
        num = self.available() - (
            (self.SERIAL_RX_BUFFER_SIZE + self._rx_buffer_head - self._rx_buffer_tail)
            % self.SERIAL_RX_BUFFER_SIZE
        )
        i = 0
        while i < num:
            j = (self._rx_buffer_head + 1) % self.SERIAL_RX_BUFFER_SIZE
            if j != self._rx_buffer_tail:
                thebs = self._read_bytes(self.REG_WK2132_FDAT, 1)
                self._rx_buffer[self._rx_buffer_head] = thebs[0]
                self._rx_buffer_head = j
                i += 1
            else:
                break
        if self._rx_buffer_head == self._rx_buffer_tail:
            return ""
        return self._rx_buffer[self._rx_buffer_tail]

    def read(self, size=1):
        """!
        @brief Read size bytes from the serial port,
        @n this operation will delete the data in the buffer.
        @param size: the bytes of read
        @return less characters as requested.
        """
        num = self.available() - (
            (self.SERIAL_RX_BUFFER_SIZE + self._rx_buffer_head - self._rx_buffer_tail)
            % self.SERIAL_RX_BUFFER_SIZE
        )
        i = 0
        k = 0
        r = []
        if size > self.available():
            size = self.available()
        while i < num or k < size:
            j = (self._rx_buffer_head + 1) % self.SERIAL_RX_BUFFER_SIZE
            if k < size and self._rx_buffer_tail != self._rx_buffer_head:
                r.append(int(self._rx_buffer[self._rx_buffer_tail]))
                self._rx_buffer_tail = (
                    self._rx_buffer_tail + 1
                ) % self.SERIAL_RX_BUFFER_SIZE
                k += 1
            if i < num and j != self._rx_buffer_tail:
                b = self._read_bytes(self.REG_WK2132_FDAT, 1)
                if len(b) != 1:
                    return -1
                self._rx_buffer[self._rx_buffer_head] = b[0]
                self._rx_buffer_head = j
                i += 1
            if k >= size and j != self._rx_buffer_tail:
                # print("ok")
                break
        try:
            return r
        finally:
            pass

        return r  # bytes(r, encoding = "utf8")

    def flush(self):
        """!
        @brief Wait for the data to be transmited completely
        """
        fsr = self._read_fifo_state_reg()
        while fsr & self.sFsrReg_tDat > 0:
            time.sleep(0.001)

    def write(self, value):
        """!
        @brief Output the given byte string over the serial port.
        @param value: byte string
        @return return bytes actually written.
        """
        # print("at@@@@@")
        # convertOk = False
        if isinstance(value, str):
            # print("string detected")
            databyte = bytes(value, "ascii")
        elif isinstance(value, int):
            # print("int detected")
            databyte = arr.array('b', bytearray([value % 0xFF]))
        else:
            databyte = value

        tx_len = length = len(databyte)
        n = 0
        writeok = False
        while tx_len > 0:
            writeok = False
            try:
                fsr = self._read_fifo_state_reg()
                if fsr & self.sFsrReg_tFull > 0:
                    print("FIFO full")
                    return length - len(databyte[n:])
                self._write_bytes(self.REG_WK2132_FDAT, [databyte[n] & 0xFF])
                n += 1
                tx_len -= 1
                writeok = True
            finally:
                pass
        if writeok is True:
            return length - len(databyte[n:])

        return 0

    def _read_fifo_state_reg(self):
        lengthbytes = self._read_bytes(self.REG_WK2132_FSR, 1)
        if len(lengthbytes) != 1:
            return 0
        return lengthbytes[0]

    def _begin(self, baud, theformat, mode, opt):
        """!
        @brief Init function, set the band rate of sub UART,
        @n data format, communication mode, and Line-Break output
        @param baud: baud rate, it support: 9600, 57600, 115200, 2400, 4800, 7200,
        @n     14400, 19200, 28800,38400, 76800, 153600, 230400, 460800, 307200, 921600
        @param format: Data format, it support:
        @n     IIC_SERIAL_8N1, IIC_SERIAL_8N2, IIC_SERIAL_8Z1,IIC_SERIAL_8Z2
        @n     IIC_SERIAL_8O1, IIC_SERIAL_8O2, IIC_SERIAL_8E1, IIC_SERIAL_8E2
        @n     IIC_SERIAL_8F1, IIC_SERIAL_8F2
        @param mode: Sub UART communciation mode, can set to UART mode,
        @n all enumeration values in eCommunicationMode_t
        @param opt: Sub UART Line-Break output control bit, can set
        @n to normal output (0) and Line-Break output (1),
        @n all enumeration values in eLineBreakOutput_t or 0/1
        @return Return 0 if init succeeds, otherwise return non-zero
        """
        self._rx_buffer_head = 0
        self._rx_buffer_tail = 0

        channel = self._sub_serial_channel_switch(self.SUBUART_CHANNEL_1)
        bytesin = self._read_bytes(self.REG_WK2132_GENA, 1)

        if len(bytesin) != 1:
            print("READ BYTE ERROR!")
            return self.ERR_READ
        if bytesin[0] & 0x80 == 0:
            print("Read REG_WK2132_GENA  ERROR!")
            return self.ERR_REGDATA
        self._sub_serial_channel_switch(channel)
        self._sub_serial_config(self._sub_serial_channel)
        self._set_sub_serial_baudrate(baud)
        self._set_sub_serial_config_reg(theformat, mode, opt)
        return self.ERR_OK

    def _sub_serial_config(self, sub_uart_channel):
        self._sub_serial_global_reg_enable(sub_uart_channel, 0)
        self._sub_serial_global_reg_enable(sub_uart_channel, 1)
        self._sub_serial_global_reg_enable(sub_uart_channel, 2)
        self._sub_serial_page_switch(0)
        sier = ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (1 << 7)) & 0xFF
        self._sub_serial_reg_config(self.REG_WK2132_SIER, sier)
        fcr = ((0 << 0) | (0 << 1) | (1 << 2) | (1 << 3) | (0 << 4) | (0 << 6)) & 0xFF
        self._sub_serial_reg_config(self.REG_WK2132_FCR, fcr)
        scr = ((1 << 0) | (1 << 1) | (0 << 2) | (0 << 3)) & 0xFF
        self._sub_serial_reg_config(self.REG_WK2132_SCR, scr)

    def _sub_serial_page_switch(self, page):
        if page > 1:
            return None
        bytesin = self._read_bytes(self.REG_WK2132_SPAGE, 1)
        if len(bytesin) != 1:
            print("READ BYTE ERROR!")
            return None
        if page == 0:
            bytesin[0] &= 0xFE
        elif page == 1:
            bytesin[0] |= 0x01
        self._write_bytes(self.REG_WK2132_SPAGE, bytesin)
        bytesin = self._read_bytes(self.REG_WK2132_SPAGE, 1)
        return page

    def _sub_serial_global_reg_enable(self, sub_uart_channel, thetype):
        if sub_uart_channel > self.SUBUART_CHANNEL_ALL:
            print("SUBSERIAL CHANNEL NUMBER ERROR!")
            return None
        reg_addr = self._get_global_reg_type(thetype)
        channel = self._sub_serial_channel_switch(self.SUBUART_CHANNEL_1)
        bytesin = self._read_bytes(reg_addr, 1)
        if len(bytesin) != 1:
            print("READ BYTE SIZE ERROR!")
            return None
        if sub_uart_channel == self.SUBUART_CHANNEL_1:
            bytesin[0] |= 0x01
        elif sub_uart_channel == self.SUBUART_CHANNEL_2:
            bytesin[0] |= 0x02
        else:
            bytesin[0] |= 0x03
        self._write_bytes(reg_addr, bytesin)
        bytesin = self._read_bytes(reg_addr, 1)
        self._sub_serial_channel_switch(channel)
        return channel

    def _get_global_reg_type(self, thetype):
        if thetype < 0 or thetype > 2:
            print("Global Reg Type Error!")
            return 0
        reg_addr = 0
        if thetype == 0:
            reg_addr = self.REG_WK2132_GENA
        elif thetype == 1:
            reg_addr = self.REG_WK2132_GRST
        else:
            reg_addr = self.REG_WK2132_GIER
        return reg_addr

    def _sub_serial_reg_config(self, reg, val):
        bytesin = self._read_bytes(reg, 1)
        if len(bytesin) != 1:
            return None
        bytesin[0] = bytesin[0] | val
        self._write_bytes(reg, bytesin)
        bytesin = self._read_bytes(reg, 1)
        return len(bytesin)

    def _sub_serial_channel_switch(self, sub_uart_channel):
        channel = self._sub_serial_channel
        self._sub_serial_channel = sub_uart_channel
        return channel

    def _set_sub_serial_baudrate(self, baud):
        scr = self._read_bytes(self.REG_WK2132_SCR, 1)
        self._sub_serial_reg_config(self.REG_WK2132_SCR, 0)
        baud1 = 0
        baud0 = 0
        baud_pres = 0
        val_intger = self.FOSC // (baud * 16) - 1
        val_decimal = (self.FOSC % (baud * 16)) // (baud * 16)
        type(val_intger)
        type(val_decimal)
        baud1 = (val_intger >> 8) & 0xFF
        baud0 = val_intger & 0x00FF
        while val_decimal > 0x0A:
            val_decimal /= 0x0A
        baud_pres = val_decimal & 0xFF
        self._sub_serial_page_switch(1)

        self._sub_serial_reg_config(self.REG_WK2132_BAUD1, int(baud1))
        self._sub_serial_reg_config(self.REG_WK2132_BAUD0, int(baud0))
        self._sub_serial_reg_config(self.REG_WK2132_PRES, int(baud_pres))

        self._sub_serial_page_switch(0)
        self._sub_serial_reg_config(self.REG_WK2132_SCR, scr[0])

    def _set_sub_serial_config_reg(self, theformat, mode, opt):
        self._addr = self._update_addr(
            self._addr, self._sub_serial_channel, self.OBJECT_REGISTER
        )
        bytesin = self._read_bytes(self.REG_WK2132_LCR, 1)
        if len(bytesin) != 1:
            print("READ BYTE ERROR!")
            return None
        lcr = bytesin[0] & 0xC0
        lcr |= theformat
        lcr |= mode << 4
        lcr |= opt << 5
        self._write_bytes(self.REG_WK2132_LCR, [lcr])
        return self._read_bytes(self.REG_WK2132_LCR, 1)

    @staticmethod
    def _update_addr(pre, sub_uart_channel, obj):
        newaddr = pre & 0xF8
        newaddr |= obj & 0x01
        newaddr |= sub_uart_channel << 1
        newaddr &= 0xFF
        return newaddr

    def _write_bytes(self, reg, buf):
        """!
        @brief write bytes to register
        @param reg  Register address 8bits
        @param buf Store buffer list for the data to be write
        """
        self.last_operate_status = self.STA_ERR_DEVICE_NOT_DETECTED
        self._addr = self._update_addr(
            self._addr, self._sub_serial_channel, self.OBJECT_REGISTER
        )

        while not self._i2c.try_lock():
            pass
        try:
            self._i2c.writeto(self._addr, bytes([reg] + buf))
            self.last_operate_status = self.STA_OK
        finally:
            self._i2c.unlock()

        if self.last_operate_status == self.STA_OK:
            return len(buf)
        return 0

    def _read_bytes(self, reg, len1):
        """!
        @brief Read bytes data from register.
        @param reg  Register address 8bits
        @param len1 Store buffer list for the data to be read
        @return Return list of data
        """
        self.last_operate_status = self.STA_ERR_DEVICE_NOT_DETECTED
        self._addr = self._update_addr(
            self._addr, self._sub_serial_channel, self.OBJECT_REGISTER
        )
        self._addr = self._addr & 0xFE

        while not self._i2c.try_lock():
            pass
        try:
            buffer = bytearray(len1)
            self._i2c.writeto_then_readfrom(self._addr, bytes([reg]), buffer)
            self.last_operate_status = self.STA_OK
        finally:
            self._i2c.unlock()

        if self.last_operate_status == self.STA_OK:
            return list(buffer)
        return []
