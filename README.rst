Introduction
============
.. image:: https://readthedocs.org/projects/circuitpython-dfrobot-gravity-drf0627-dual-uart/badge/?version=latest
    :target: https://circuitpython-dfrobot-gravity-drf0627-dual-uart.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord
.. image:: https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/workflows/Build%20CI/badge.svg
    :target: https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/actions
    :alt: Build Status
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for DFROBOT Gravity: I2C to Dual UART Module

Note: this library only uses polled communications so it is important that your project is designed to frequently check for received data. This library is useful for communication with systems with a command/response interaction with the device. The Internal FIFO is 256 bytes long and therefore it should handle many use cases. It is for use in CircuitPython and interrupts are not supported (to my knowledge). It is possible a MicroPython version could support this and this project may be forked to support this (once the author learns more about that enviroment).

.. image:: https://user-images.githubusercontent.com/70548834/187725830-5e979aee-c291-4bbb-9eaa-9b412f353efd.jpg
    :width: 400
    :target: https://www.dfrobot.com/product-2001.html
    :alt: Gravity: I2C to Dual UART Module (SKU:DFR0627)

* `Gravity: I2C to Dual UART Module (SKU:DFR0627) <https://www.dfrobot.com/product-2001.html>`_
* `Extra Wiki information  <https://wiki.dfrobot.com/Gravity%3A%20IIC%20to%20Dual%20UART%20Module%20SKU%3A%20DFR0627>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `DFROBOT Gravity: I2C to Dual UART Module Hardware <https://www.dfrobot.com/product-2001.html>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/>`_.
To install for current user:

.. code-block:: shell

    pip install CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip install CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart

To install in a virtual environment in your current project:

.. code-block:: shell

    python -m venv TestEnviromentDirectory (Name it whatever you want)
    cd TestEnviromentDirectory
    pip install CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============
.. code-block::

    import time
    import board
    import circuitpython_dfrobot_gravity_drf0627_dual_uart as DualUart

    i2c = board.I2C()


    uart1 = DualUart.DFRobot_IIC_Serial(
        i2c,
        sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_1,
        IA1=1,
        IA0=1,
    )

    uart2 = DualUart.DFRobot_IIC_Serial(
        i2c,
        sub_uart_channel=DualUart.DFRobot_IIC_Serial.SUBUART_CHANNEL_2,
        IA1=1,
        IA0=1,
    )

    try:
        uart1.begin(9600, uart1.IIC_Serial_8N1)
        print("Opened: UART 1 ")
    finally:
        pass

    try:
        uart2.begin(9600, uart2.IIC_Serial_8N1)
        print("Opened: UART 2")
    finally:
        pass

    sendID = 1
    sendDelayCount = 1

    while True:
        time.sleep(0.3)
        sendDelayCount -= 1
        if sendDelayCount <= 0:
            sendDelayCount = 10
            uart1.write("From1:" + str(sendID))
            uart2.write("From2:" + str(sendID))

        if uart1 is not None:
            if uart1.available():
                s = ""
                while uart1.available():
                    b = uart1.read(1)
                    s += chr(b[0])
                print("<1:" + s + " len:" + str(len(s)) + ">")

        if uart2 is not None:
            if uart2.available():
                s = ""
                while uart2.available():
                    b = uart2.read(1)
                    s += chr(b[0])
                print("<2:" + s + " len:" + str(len(s)) + ">")

Additional connection information
=================================
The DRF0627 comes with a cable that allows for connection to the CircuitPython hardware using a
SparkFun STEMMA QT / Qwiic Breadboard Breakout Adapter Product ID: 4527 https://www.adafruit.com/product/4527

.. image:: https://user-images.githubusercontent.com/70548834/187724117-4660a9b5-e877-4bf8-8dbe-a0c5a8d7ca6e.jpg
    :width: 200
    :target: https://www.adafruit.com/product/4527
    :alt: SparkFun STEMMA QT / Qwiic Breadboard Breakout Adapter

Connections:
************
.. code-block::

    Black wire -> Stemma Ground
    Red wire -> Stemma 3.3 V
    Green wire -> Stemma SDA
    Blue wire -> Stemma SCA

To test the connection the "t" and "R" pins can be connected together. If you tie the "T" and "R" pins between the same UART the data will echo back to you on the same port. If you tie the "T" and "R" pins from UART1 to UART 2 data will be send between the two ports.

If RS485 is desired you can use a RS485 adapter such as the "SCM TTL to RS-485 Interface Module"

.. image:: https://user-images.githubusercontent.com/70548834/187728623-31a28fc7-3a15-42c7-ad91-6f9be4e81756.jpg
    :width: 400
    :target: https://protosupplies.com/product/scm-ttl-to-rs-485-interface-module/
    :alt: SCM TTL to RS-485 Interface Module

IC2 Addressing:
***************
There are two address dip switches A1 and A0. The standard (factory setting is both switched to "ON")

.. code-block::

    A1 = ON,   A0 = ON  : Address 0x70-0x77
    A1 = ON,   A0 = OFF : Address 0x50-0x57
    A1 = OFF,  A0 = ON  : Address 0x30-0x37
    A1 = OFF,  A0 = OFF : Address 0x10-0x17


Additional Documentation
========================
API documentation for this library can be found on `Read the Docs <https://pypi.org/project/circuitpython-dfrobot-gravity-drf0627-dual-uart/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

For information on the chip used on this board (WK2132), please check out (original)
`WK2132_DS_CN_V011_2017_5_.pdf <https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/files/9471826/WK2132_DS_CN_V011_2017_5_.pdf>`_.

`WK2132_English.pdf <https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/files/9471834/WK2132_English.pdf>`_.


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_Dual_Uart/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
