"""
Generates random quantum state, then maps the argument of each Fock coefficient
to a colour in RGB space, and saves the result to a file.
"""
import os
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
    colour = colorsys.hsv_to_rgb(h, 1.0, 1.0) # Convert HSV space -> RGB space

    # Coloursys returns RGB values as floats in [0, 1]. Convert to ints in [0, 255]
    colour = tuple(int(np.round(i * 255)) for i in colour)

    return colour

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

    # Construct path to output directory
    this_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(this_dir, os.pardir)
    output_dir = os.path.join(parent_dir, "output")
    # Create output dir if it doesn't exist
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Save arguments and colours to files (args useful for debugging)
    colours_fname = os.path.join(output_dir, 'colours.npy')
    np.save(colours_fname, colours)
    print("Colours saved to " + os.path.relpath(colours_fname, parent_dir))
    state_fname = os.path.join(output_dir, 'state.npy')
    np.save(state_fname, args)
    print("State saved to " + os.path.relpath(state_fname, parent_dir))
