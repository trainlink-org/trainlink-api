function initiateTrainLink(ipAddress) {
	websocket = new WebSocket(ipAddress);
	websocket.onmessage = function (event) {
		data = JSON.parse(event.data);
		if (data.type == "config") {
			/*Set up config variables here*/
			try{
				config(data);
			} catch (err) {
				throw("Error - Config function missing!")
			}
	 	} else if (data.type == "state") {
			update(data);
			try {
				update(data);
			} catch (err) {
				throw("Error - Update function missing!");
			}
		}
	}
}

function setSpeed(address, speed, direction=-1) { 
	/*	Address: the loco address
		Speed: New speed for loco
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
}

function stopCab(address) {
	websocket.send(JSON.stringify({class: "cabControl", action: "stop", cabAddress: address}));
}

function estopCab(address) {
	websocket.send(JSON.stringify({class: "cabControl", action: "estop", cabAddress: address}));
}

function sendCommand(command) {
	websocket.send(JSON.stringify({class: "directCommand", command: command}));
}

function setPower(state) {
	websocket.send(JSON.stringify({class: "power", state: state}));
}