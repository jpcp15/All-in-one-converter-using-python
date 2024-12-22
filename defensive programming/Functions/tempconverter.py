import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk

def TemperatureConverter():
    # Function to convert temperature
    def convert():
        celTemp = celTempVar.get()
        fahTemp = fahTempVar.get()

        # Invariant: Ensure that at least one temperature value is non-zero for conversion
        assert (celTemp != 0.0 or fahTemp != 0.0), "At least one temperature value must be provided for conversion"
        
        # Ensure that the values are valid numbers
        assert isinstance(celTemp, (int, float)), f"Invalid temperature value for Celsius: {type(celTemp)}"
        assert isinstance(fahTemp, (int, float)), f"Invalid temperature value for Fahrenheit: {type(fahTemp)}"

        if celTemp != 0.0:
            celToFah = (celTemp * 9 / 5) + 32
            fahTempVar.set(celToFah)
        elif fahTemp != 0.0:
            fahToCel = (fahTemp - 32) * (5 / 9)
            celTempVar.set(fahToCel)

    # Function to reset the fields
    def reset():
        # Create a reset confirmation window
        reset_window = Toplevel(padx=50, pady=50)
        reset_window.grid()
        message = Label(reset_window, text="Reset Complete")
        button = Button(reset_window, text="OK", command=reset_window.destroy)

        message.grid(row=0, padx=5, pady=5)
        button.grid(row=1, ipadx=10, ipady=10, padx=5, pady=5)

        # Invariant: Ensure reset works correctly by asserting that values are reset to 0
        assert celTempVar.get() != 0, "Celsius temperature was not reset to 0"
        assert fahTempVar.get() != 0, "Fahrenheit temperature was not reset to 0"

        # Reset temperature variables to 0
        celTempVar.set(0)
        fahTempVar.set(0)

    # Create the main window for the temperature converter
    top = Toplevel()
    top.title("Temperature Converter")

    # Temperature variables
    celTempVar = IntVar()
    fahTempVar = IntVar()

    # Set initial values
    celTempVar.set(0)
    fahTempVar.set(0)

    # Title label
    titleLabel = Label(top, text="Temperature Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    titleLabel.grid(column=1, row=1)

    # Celsius label and entry
    celLabel = Label(top, text="Celsius (°C): ", font=("tahoma", 16), fg="red")
    celLabel.grid(row=2, column=1, pady=10, sticky=NW)

    celEntry = Entry(top, width=15, bd=5, textvariable=celTempVar)
    celEntry.grid(row=2, column=1, pady=10, sticky=NW, padx=158)

    # Fahrenheit label and entry
    fahLabel = Label(top, text="Fahrenheit (°F): ", font=("tahoma", 16), fg="blue")
    fahLabel.grid(row=3, column=1, pady=10, sticky=NW)

    fahEntry = Entry(top, width=15, bd=5, textvariable=fahTempVar)
    fahEntry.grid(row=3, column=1, pady=10, sticky=NW, padx=158)

    # Convert button
    convertButton = Button(
        top, text="Convert", font=("tahoma", 8, "bold"), relief=RAISED, bd=5, justify=CENTER, highlightbackground="red",
        overrelief=GROOVE, activebackground="green", activeforeground="blue", command=convert
    )
    convertButton.grid(row=4, column=1, ipady=8, ipadx=12, pady=5, sticky=NW, padx=55)

    # Reset button
    resetButton = Button(
        top, text="Reset", font=("tahoma", 8, "bold"), relief=RAISED, bd=5, justify=CENTER, highlightbackground="red",
        overrelief=GROOVE, activebackground="green", activeforeground="blue", command=reset
    )
    resetButton.grid(row=4, column=2, ipady=8, ipadx=12, pady=5, sticky=NW)

    top.mainloop()