function trainlink() {
	function initiateTrainLink(ipAddress) {
		/*	ipAddress: the ip address of the server */

		/* Creates a websocket connected to the server */
		websocket = new WebSocket(ipAddress);
		/* what to do when a new message is recived */
		websocket.onmessage = function (event) {
			data = JSON.parse(event.data);
			if (data.type == "config") {
				try{
					config(data);
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
		
		/* Sends the packet to the API server */
		websocket.send(JSON.stringify({class: "cabControl", action: "setSpeed", cabAddress: address, cabSpeed: speed, cabDirection: direction}));
		console.log(JSON.stringify({class: "cabControl", action: "setSpeed", cabAddress: address, cabSpeed: speed, cabDirection: direction}))
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
		console.log(JSON.stringify({class: "directCommand", command: command}))
	}

	function setPower(state) {
		/* state: the state to set the track power to (0 - off, 1 - on) */

		/* Sends track power packet to the API server */
		websocket.send(JSON.stringify({class: "power", state: state}));
	}
	trainlink.initiateTrainLink = initiateTrainLink;
	trainlink.setSpeed = setSpeed;
	trainlink.stopCab = stopCab;
	trainlink.estopCab = estopCab;
	trainlink.sendCommand = sendCommand;
	trainlink.setPower = setPower;
}