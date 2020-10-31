function trainlink() {
	function initiateTrainLink(ipAddress='192.168.1.158', port='6789') {
		/*	ipAddress: the ip address of the server */

		/* Creates a websocket connected to the server */
		websocket = new WebSocket("ws://"+ipAddress+":"+port);
		/* what to do when a new message is recived */
		websocket.onmessage = function (event) {
			data = JSON.parse(event.data);
			if (data.type == "config") {
				try{
					config(data);
					debug = data.debug.toLowerCase();
					if (debug == "true") {
						console.log("Debug enabled")
					}
				} catch (err) {
					throw("Error - Config function missing!")
				}
			} else if (data.type == "state") {
				try {
					update(data);
				} catch (err) {
					throw("Error - Update function missing!");
				}
			}
		}
	}

	function setSpeed(address, speed, direction=-1) { 
		/*	address: the cab address
			speed: New speed for cab
			direction: set direction
		*/

		/*	The name associated with the train can be used instead of the numerical address */
		
		/*	There are two ways to change the direction of the current train.
			1. Use the direction parameter
			2. Use the value of the slider (minus values reverse)
			
			The following logic accounts for these
		*/
		if (direction == -1) {
			if (speed < 0) {
				direction = 0;
				speed = String(speed)
				speed = speed.substring(1)
			}
			else if (speed >= 0){
				direction = 1;
			}
			
		}

		outputDirection = parseInt(direction, 10)
		outputSpeed = parseInt(direction, 10)

		if (direction < -1 || direction > 1 || Number.isNaN(outputDirection)) {
			if (debug) {
				console.warn("Unallowed direction!")
			}
		} else if (speed > 126 || speed < -1 || Number.isNaN(outputSpeed)){
			if (debug) {
				console.warn("Unallowed speed!")
			}	
		}else if (address < 0) {
			if (debug) {
				console.warn("Unallowed address!")	
			}
		} else {
		
			/* Sends the packet to the API server */
			websocket.send(JSON.stringify({class: "cabControl", action: "setSpeed", cabAddress: address, cabSpeed: speed, cabDirection: direction}));
		}
	}

	function stopCab(address) {
		/*	adress: the address of the cab to stop */

		/* Sends stop packet to the API server */
		websocket.send(JSON.stringify({class: "cabControl", action: "stop", cabAddress: address}));
	}

	function estopCab(address) {
		/*	adress: the address of the cab to stop */

		/* Sends emergency stop packet to the API server */
		websocket.send(JSON.stringify({class: "cabControl", action: "estop", cabAddress: address}));
	}

	function sendCommand(command) {
		/*	command: the command to send to the base station */

		/* Sends direct command packet to the API server */
		websocket.send(JSON.stringify({class: "directCommand", command: command}));
	}

	function setPower(state) {
		/* state: the state to set the track power to (0 - off, 1 - on) */

		/* Sends track power packet to the API server */
		websocket.send(JSON.stringify({class: "power", state: state}));
	}

	function cabFunction(cab, func, state=-1) {
		websocket.send(JSON.stringify({class: "cabFunction", cab: cab, func: func, state: state}));
	}

	trainlink.initiateTrainLink = initiateTrainLink;
	trainlink.setSpeed = setSpeed;
	trainlink.stopCab = stopCab;
	trainlink.estopCab = estopCab;
	trainlink.sendCommand = sendCommand;
	trainlink.setPower = setPower;
	trainlink.cabFunction = cabFunction;
}