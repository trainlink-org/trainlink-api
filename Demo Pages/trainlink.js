function initiateTrainLink(address) {
	
}

function setSpeed(address, speed, localDirection=-1) { 
	/*	Address: the loco address
		Speed: New speed for loco
		localDirection: set direction
	*/
	
	/*	There are multiple ways to change the direction of the current train.
		1. Use the localDirection parameter
		2. Use the global variable direction
		3. Use the value of the slider (minus values reverse)
		
		The following logic accounts for these
	*/
	if (localDirection == -1) {
		try {
			localDirection = direction;
		}
		catch (err) {
			if (speed < 0) {
				localDirection = 0;
			}
			else if (speed >= 0){
				localDirection = 1;
			}
		}
	}
	
	/* Sends the packet to the API server */
	websocket.send(JSON.stringify({action: "setSpeed", locoAddress: address, locoSpeed: speed, locoDirection: direction}));
}