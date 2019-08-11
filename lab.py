"""
Generates random quantum state, then maps the argument of each Fock coefficient
to a colour in RGB space, and saves the result to a file.
"""

import colorsys
from typing import Tuple
import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *

# Colour in RGB space
Colour = Tuple[int, int, int]

def displaced_squeezed(alpha: complex, z: complex) -> sf.program.Program:
    """
    Returns a `strawberryfields.program.Program` instance that creates a
    displaced squeezed state $|\alpha, z>$.
    """
    program = sf.Program(1)
    with program.context as q:
        Dgate(alpha) | q[0]
        Sgate(z) | q[0]
    return program

def run_program(prog: sf.program.Program, cutoff: int=72) -> np.ndarray:
    """
    Runs a `strawberryfields.program.Program` and returns the output state
    vector in the Fock basis.
    """
    eng = sf.Engine('fock', backend_options={ 'cutoff_dim': cutoff })
    result = eng.run(prog)
    return result.state.data

def rand_complex(max_mod: float=1.0) -> complex:
    """Returns a random complex number with `|z| < max_mod`"""
    r = np.random.rand() * max_mod
    theta = np.random.rand() * 2 * np.pi
    return r * np.exp(1j * theta)

def arg_to_colour(theta: float) -> Colour:
    """Maps the argument of a complex number to a colour"""
    h = (theta / np.pi) + 1 # Map [-π, π] -> [0, 1] - Hue in HSV space
    h /= 2 # Map [0, 1] -> [0, 0.5] - Better colour map than [0, 1]
    return colorsys.hsv_to_rgb(h, 1.0, 1.0) # Convert HSV space -> RGB space

if __name__ == '__main__':
    # TODO: Implement circuits that produce different types of state

    # Generate random state parameters
    alpha = rand_complex(1.0)
    z = rand_complex(1.0)
    # Circuit that produces a general Gaussian state
    circuit = displaced_squeezed(alpha, z)

    # Run circuit
    print("Running circuit...")
    state = run_program(circuit)
    print("Done")

    # Arguments of each Fock coefficient
    args = np.angle(state)

    # Convert arguments to RGB colours
    colours = list(map(arg_to_colour, args))

    # Save arguments and colours to files (args useful for debugging)
    np.save('colours.npy', colours)
    print("Colours saved to colours.npy")
    np.save('state.npy', args)
    print("State saved to state.npy")
