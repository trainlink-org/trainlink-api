# TrainLink API
[![Downloads (github)](https://img.shields.io/github/downloads/matt-hu/trainlink-api/total)](https://img.shields.io/github/downloads/matt-hu/trainlink-api/total)
[![Documentation Status](https://readthedocs.org/projects/trainlink-api/badge/?version=latest)](https://trainlink-api.readthedocs.io/en/latest/?badge=latest)

__Please note: This is still undergoing intial development and not all links etc. are guarenteed to work!__  
 This is an API to intergrate with a DCC++ (or DCC++ EX) BaseStation. It provides a simple way to control it over your local network, with multiple instances supported. This means if you open a website using TrainLink on two devices connected to the same server, they will be kept in sync!

 ## What is in this Repository?
 In this repository you will find the following (the sublist shows supported platforms, whilst ones in italic are planned for the future):
* The API Server
    * Python (Cross-platform)
    * _Arduino (ESP32/ESP8266)_
* The API Library
    * Javascript (Cross-platform)
    * _Arduino_
    * _Python_
* A Demo page

## Why should I use TrainLink?
One of the major features of TrainLink is the cross-platform nature of the API. The server runs on Python, meaning it can be run on most platforms. Also, the API library is written in Javascript, so again, it can be run on most platforms.

Also, TrainLink is very flexible to different development styles. For example, if you don't need the sync feature, you can just send direct commands.

## Getting Started
### What you need to install
1. First, you need to download the latest version of the API from this repository from the releases section (for more information, see the _Releases and Branches_ section below)
1. After that, to run the server you will need Python installed on your PC. The latest version of Python is recommended, versions 3.7 and 3.8 have been tested. However, this is not to say other versions won't work. You can download Python [here](https://www.python.org/downloads/).  
__Note:__ When installing Python, make sure to check 'Add Python to Path'
![How to enable add python to path](https://github.com/matt-hu/trainlink-api/blob/master/Documentation/Images/install-python-path.jpg)

1. Next, you need to install the required packages that the server needs. These are:
    * [Websockets](https://pypi.org/project/websockets/)
    * [Serial](https://pypi.org/project/pyserial/) 
    * [XMLtoDict](https://pypi.org/project/xmltodict/) 

    These can be installed via _reqirements.txt_, or alternativly via pip individually. To use _requirements.txt_, change into the directory where you downloaded the release then run:
    ```console
    $ pip install -r requirements.txt
    ```
1. Your TrainLink installation is done! If you want to try out the demo page, start by running the server, then go into the Demo Pages folder and open `DemoPage.html`.

For more information on configuring the server, head to the [readthedocs page](https://trainlink-api.readthedocs.io/en/latest/api-usage.html)

## Compatible front ends
Here is a list of compatable front ends that work with TrainLink:
Name | Location | Maintainer
-----|----------|-----------
Demo page | This repository | [Matt-hu](https://github.com/matt-hu)  

Its looking a little bare at the moment! If you know of or maintain a compatible front end, please let me know and I wil add it here.  
You can identify compatible front ends from this logo:  
[![Trainlink compatible icon](https://github.com/matt-hu/trainlink-api/blob/master/Documentation/Images/compatible-icon-small.png)](https://matt-hu.github.io/trainlink-api)

## What features are supported?
For the full list of supported features and commands, please see the wiki and full documentation. Here is a brief list of what is currently __fully__ supported:
Feature | Version
--------|--------
Cab control | 0.1
Track power control | 0.1
Direct command | 0.1

The reason I say fully supported is because the API has the direct command function. This allows DCC++ comands (such as `<t 1 3 126 1>`) to be sent directly to the base s tation, so all DCC++ commands are supported to some degree. Full support means they are handled by the server and are synced between instances.

To find out what is next for TrainLink, check out the [Development Tasks](https://github.com/matt-hu/trainlink-api/projects/1) project!

## Branches and releases
Releases are numbered according to the [Semantic Numbering](https://semver.org/) scheme. Therefore, releases will be numbered as following:

>Given a version number MAJOR.MINOR.PATCH, increment the:
>
>MAJOR version when you make incompatible API changes,  
MINOR version when you add functionality in a backwards compatible manner, and  
PATCH version when you make backwards compatible bug fixes."

### Branches
Master branch - Where code for the next release accumulates  
Preview branch - Code that is finished, but not fully tested yet  
Development-x.x branch - Where I write my code, almost guaranteed to be unstable!

## Contributing
Want to suggest a feature, found a bug, or even better, fixed a bug? Please, go ahead and submit a pull request or issue! Every little helps, and even the smallest contribution will go a long way to help me with this project. You don't need to know how to code, as correcting typos or updating the documentation would help a lot! For more information on contributing, please see the wiki.

## More Information
For more information please see the following:
* [The wiki](https://github.com/matt-hu/trainlink-api/wiki) - FAQ and other repository maintainance help
* [Readthedocs](https://trainlink-api.readthedocs.io) - information on the API itself and the function calls

Many thanks,  
Matt  
\- September 2020
