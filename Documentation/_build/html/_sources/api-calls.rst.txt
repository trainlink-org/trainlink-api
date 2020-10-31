=========
API Calls
=========
This page details the calls available to programmers using the API on each platform.

Javascript Client
=================
This is the library used for developing web applications.
Due to the use of Javascript, pages written using this method can be run as files, rather than in a server.

.. module:: trainlink

.. method:: initateTrainLink(ipAddress="127.0.0.1", port="6789")

    :param ipAddress:
        The local IP address of the server (127.0.0.1 restricts access to local machine only).
    
    :param port:
        The port of the server (6789 is the default).

    Creates a link with a DCC++ BaseStation. If the server is running on your local machine, you can use ``127.0.0.1``.
    Otherwise, use the IP address or hostname of the server. I recommend setting up a static IP for this machine or using
    it's hostname.

.. method:: setSpeed(address, speed, direction=-1)

    :param address:
        The address of the cab that you want to change the speed of

    :param int speed:
        The new speed for the cab

    :param int direction:
        The direction for the cab. If the direction is set to -1, then the polarity of the speed value is used to set the direction.
        If the value of speed is negative, the cab will reverse. Likewise, if the speed is positive the cab will go forwards.
    
    Sets the speed of the given cab. This function is very flexible as you can use either the direction argument or the 
    polarity of the speed to change the direction. Also, for address, either the numerical decoder-set address can be used, or alternativly,
    the phonetic name set in the server's ``config.xml``.

.. method:: stopCab(address)

    :param address:
        The address of the cab that you want to stop
    
    Stops the cab using the deceleration value set in the decoder. Like *setSpeed*, there are two ways of choosing the address. Refer to 
    the setSpeed description for more details.

.. method:: eStopCab(address)

    :param address:
        The address of the cab that you want to stop

    Stops the cab **instantly**, ignoring the deceleration value set in the decoder. Like *setSpeed*, there are two ways of choosing the address. Refer to 
    the setSpeed description for more details.

.. method:: sendCommand(command)

    :param command:
        The command that will be sent to the BaseStation

    Sends a command directly to the BaseStation. An example command would be ``<t 1 3 126 1>``.

.. method:: setPower(state)

    :param state:
        The power state the track will be set to (0 - off, 1 - on)

    Changes whether power is applied to both the programming and main tracks. No power = no movement!

.. method:: cabFunction(address, function, state=-1)

    :param address:
        The address of the cab you want to change the function of
    
    :param int function:
        The function number to change (e.g. 0)

    :param state:
        The state to set the funtion to. 0 is off, 1 is on and -1 (the default state) toggles the function.

    Changes a function for a cab. An example of this is lights and sounds (if a DCC sound decoder is fitted). Like the
    other functions, both the phonetic name and DCC address can be used for the address