"""Plots the results generated by lab.py as a coloured bar chart"""
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    args = np.load('state.npy')
    colours = np.load('colours.npy')

    plt.bar(range(len(args)), args, color=colours)
    plt.show()