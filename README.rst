![DRF0627](https://user-images.githubusercontent.com/70548834/187724082-bbbdea34-60d7-4014-963c-f721ea7050a6.jpg)
![Breakout](https://user-images.githubusercontent.com/70548834/187724117-4660a9b5-e877-4bf8-8dbe-a0c5a8d7ca6e.jpg)
![HiLetgo](https://user-images.githubusercontent.com/70548834/187724152-69504123-93cf-4ca5-9650-d5c197ea666d.jpg)


Introduction
============

.. image:: https://dfimg.dfrobot.com/store/data/DFR0627/DFR0627-detail-004_564x376.jpg

.. image:: https://readthedocs.org/projects/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart/badge/?version=latest
    :target: https://CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart/workflows/Build%20CI/badge.svg
    :target: https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for DFROBOT Gravity: I2C to Dual UART Module

.. image:: https://dfimg.dfrobot.com/store/data/DFR0627/DFR0627-detail-004_564x376.jpg
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
PyPI <https://pypi.org/project/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart/>`_.
To install for current user:

.. code-block:: shell

    pip3 install CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============
.. code-block::

    """ QuadRelayTest """
    # QuadRelayTest: Copyright (c) 2022 Graham Beland
    #
    # SPDX-License-Identifier: MIT
    # import the CircuitPython board and busio libraries
    import time as tm
    # CircuitPython board
    import board
    # the sparkfun_qwiicquadsolidstaterelay
    import sparkfun_qwiicquadsolidstaterelay

    # Create bus object using the board's I2C port
    i2c = board.I2C()

    # Note: default i2c address is 8
    theRelay = sparkfun_qwiicquadsolidstaterelay.Sparkfun_QwiicQuadSolidStateRelay(i2c)
    print("Opened: Relay Controller")
    if theRelay.connected:
        print("Relay connected. ")
        theRelay.relay_on(1)
        tm.sleep(1)
        theRelay.relay_off(1)
    else:
        print("Relay does not appear to be connected. Please check wiring.")


Additional connection information
=================================
The DRF0627 comes with a cable that allows for connection to the CircuitPython hardware using a 
SparkFun STEMMA QT / Qwiic Breadboard Breakout Adapter Product ID: 4527 https://www.adafruit.com/product/4527

Connection
Black wire -> Stemma Ground
Red wire -> Stemma 3.3 V
Green wire -> Stemma SDA
Blue wire -> Stemma SCA

To test the connection the "t" and "R" pins can be connected together. If you tie the "T" and "R" pins between the same UART the data will echo back to you on the same port. If you tie the "T" and "R" pins from UART1 to UART 2 data will be send between the two ports.

If RS485 is desired you can use a RS485 adapter such as the "HiLetgo 5pcs TTL to RS485 485 to Serial UART Level Reciprocal Hardware Automatic Flow Control UART to RS485 Converter RS485 to TTL" 

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/gbeland/CircuitPython_DFRobot_Gravity_DRF0627_I2C_Dual_Uart/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
