# Trainlink specification - User-facing client (High level)
*Version 0.3.0*

This is the specification to use if you are writing a user-facing interface using a Trainlink client library.


Within this specification there are a number of 'modules' that you can use. Some are compulsary, wheras some are optional (this will make sense when you start reading). Also, within each 'module' there are features that make up that module. Again, some of the features must be included for your software to be Trainlink compatible, some are optional.

# Module overview
This is an overview of the modules that make up a Trainlink implementation. See further down for more detailed information on the features that make up a module.

**Compulsary modules:**

- Update and Configuration
- Track power
- Cab speed control

**Optional modules:**

- Cab functions
- Point motors

# Compulsary modules

## Update and configuration
### **Configuration function**
You must include a configuration function to handle the initial data sent from the server. This includes information on the server configuration, such as whether debug messages are enabled. If your application shows debug messages (either via the console or other means), you should respect this value sent from the server **by default**.

### **Update function**
This function will be called every time the server sends out an update packet. This function will need to use the data sent to update any UI elements such as speed dials to show the new speed. 
## Track power

## Cab speed control


# Optional modules

## Cab functions

## Point motors