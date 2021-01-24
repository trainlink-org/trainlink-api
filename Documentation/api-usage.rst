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

Using TrainLink for Websites
============================
TrainLink for Websites uses javascript to communicate with the webserver. This gives the benefit of the 
page being able to constantly update, even after the webpage has loaded.

Adding the .js to your code
---------------------------
To enable access to all the TrainLink functions, you need to add one line of code to the top of your body in
each HTML file where the functions are needed. The line of code is this:

.. sourcecode:: html

    <script src="path/to/trainlink.js"></script>

I recommend putting the ``trainlink.js`` file in a folder named something like *js*.
In which case, your path to the .js would be ``js/trainlink.js``. ``trainlink.js`` can be found in *API Libraries/TrainLink for Websites* in the file structure you downloaded from
the TrainLink API GitHub page. If you haven't done this yet head to :doc:`/getting-started`.

Setting up your code for TrainLink
----------------------------------
Now you have added the ``trainlink.js`` to your page, you can access all the API functions as long as you call ``trainlink()``.
If you want more information on how to do this, have a look at :doc:`/api-calls`.
There are a couple of compulsory functions that you need in your code at some point and these are ``update()`` and ``config()``.
They should be structured like this:

.. sourcecode:: javascript

    function config(data) {
        /* Code to be run when a connection is establised to the server */
    }

    function update(data) {
        /* Code to be run when the server sends an update packet */
    }

Contents of the data variable
"""""""""""""""""""""""""""""

data.updateType will store the type of update that the packet is.

+-----------+---------------------+-------------------------------------------------------+
|Update type|Data values available|Usage                                                  |
+===========+=====================+=======================================================+
|"cab"      |data.cab             |Stores the address of the cab that the packet refers to|
|           +---------------------+-------------------------------------------------------+
|           |data.speed           |Stores the new speed of the cab                        |
|           +---------------------+-------------------------------------------------------+
|           |data.direction       |Stores the direction of the cab                        |
+-----------+---------------------+-------------------------------------------------------+
|"power"    |data.state           |The current state of the trackpower                    |
+-----------+---------------------+-------------------------------------------------------+
|"points"   |data.points          |An array with the current state of the points          |
+-----------+---------------------+-------------------------------------------------------+
|"config"   |data.cabs            |A list of all the cabs defined in the xml              |
|           +---------------------+-------------------------------------------------------+
|           |data.debug           |If debug is enabled in the server config.xml           |
+-----------+---------------------+-------------------------------------------------------+

Although a list of defined cabs is provided to the client when they connect, you can still address cabs not on the list.
These will be added to the internal arrays when you first use each address.