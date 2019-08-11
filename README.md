# Quantum LED
Generates a random quantum state, then displays a visual representation of it
on an AdaFruit DotStar LED strip using an Arduino.

## What It Does
The script at [quantumled/lab.py]() will generate a random
[Gaussian State](https://strawberryfields.readthedocs.io/en/latest/conventions/states.html#gaussian-states)
using [Strawberry Fields](https://strawberryfields.readthedocs.io/en/latest/index.html).
It then maps the argument of each Fock basis coefficient to a colour. These
colours are sent to an Arduino and displayed on an
[Adafruit DotStar RGB LED strip](https://learn.adafruit.com/adafruit-dotstar-leds/overview).

## Usage
1. Install the Adafruit DotStar Arduino library and hook up the DotStar strip, as
explained [here](https://learn.adafruit.com/adafruit-dotstar-leds/arduino-library-installation).

2. Flash the script at [sketch/sktetch.ino]() to the Arduino.

3. Install the required Python packages `pip install -r requirements.txt`.

4. Run `python quantumled/lab.py` to generate a random state. The state and 
colour data will be saved to the `output/` folder.

5. Run `python quantumled/comm.py` to send the colour data to the Arduino
via serial.

## TODO
- [ ] Create a web server that serves the colour data as JSON
- [ ] Get Arduino to poll web server and update LEDs
- [ ] Periodically run `lab.py` to generate a new random state
- [ ] Update `lab.py` to produce different types of state (non-Gaussian ones)