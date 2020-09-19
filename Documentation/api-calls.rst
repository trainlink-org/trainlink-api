=========
API Calls
=========
This page details the calls available to programmers using the API on each platform.

Javascript Client
=================
.. module:: trainlink

.. method:: initateTrainLink(ipAddress="127.0.0.1", port="6789")

    :param ipAddress:
        The local ip address of the server (127.0.0.1 restricts access to local machine only).
    
    :param port:
        The port of the server (6789 is the default).


.. method:: setSpeed(address, speed, direction=-1)

    :param address:
        The address of the cab that you want to change the speed of

    :param int speed:
        The new speed for the cab

    :param int direction:
        The direction for the cab. If the direction is set to -1, then the polarity of the speed value is used to set the direction.
        If the value of speed is negative, the cab will reverse. Likewise, if the speed is positive the cab will go forwards.

