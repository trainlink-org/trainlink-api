=============
Using the API
=============
This page details general usage of the API and how to implement it into your code.

Configuring the Server
======================
The server is configured using the file called ``config.xml``. Here is how to use this file:

Cabs
----
In this section, you can define a cab to add a phonetic name to use instead the DCC address set up in the decoder's CV.
Cabs are defined in the format:

.. sourcecode:: xml

    <cab>
        <name>name of train</name>
        <address>train address</address>
    </cab>

You can delete the default ``Train1`` and ``Train2`` profiles, these are just included for testing and example purposes.

Server core
-----------
This is where the ports etc for the server are set up.

ip
""
Controls the IP addresses the server will listen to connections on

.. sourcecode:: xml

    <!-- sets ip to 0.0.0.0 (all connections) -->
    <ip>auto</ip> 

    <!-- sets ip to 127.0.0.1 (local only) -->
    <ip>local</ip>

port
""""
Controls the TCP/IP port the server listens for connections on

.. sourcecode:: xml

    <!-- sets the port to 6789  -->
    <port>auto</port> 

    <!-- sets the port to 1234 -->
    <port>1234</port>

serialPort
""""""""""
Controls which serial port the server attempts to contact the DCC++ BaseStation on.

.. sourcecode:: xml

    <!-- sets the port to COM1 -->
    <serialPort>COM1</serialPort>

Debug
-----
This controls whether the debug statements are enabled or not.
If ``enableDebug`` is set to *True*, then debug statements will be showen in both the server output
and also the console in the browser (accesible via F12 on most browsers, otherwise look for *developer tools*).

