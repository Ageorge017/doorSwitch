# PicoW Door Switch
## Pinout
Reed switch leads are connected to PIN 19/GP14 and GND.
LEDs annode on pin 15 via 220Ω resistor and GND.

## Prerequisites
MicroPico extension

## Running the project
Simply plug in pico, and hit Run at the bottom

When the Raspberry Pi Pico powers up, it looks for two specific files in order:

boot.py (System setup - usually don't touch this)

main.py (Your user code)
If it finds a file named main.py, it runs it immediately.

Look at the bottom status bar for the "Upload" button (usually an arrow pointing up), OR...

Right-click anywhere inside the code window and select "MicroPico: Upload current file to Pico".

Check the "MicroPico Console" at the bottom. It should confirm that the file was uploaded/transferred.

## LEDS
### Red LED
The led will turn on if any errors are encountered
- flashing led = Fatal, needs reset
- solid led = Encountered errors, check logs

On FATAL errors, message queue is saved to file.

### Green LED
The led flashes when publishing to the mqtt server

### Reset
on reset the red led will flash twice. The Red led will flash twice followed by 2 flashes of the green led to indcate main.py start