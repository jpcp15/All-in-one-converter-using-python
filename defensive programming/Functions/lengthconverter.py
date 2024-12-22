import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk

def LengthConverter():
    # Conversion factors for various length units (in meters)
    factors = {
        'nmi': 1852, 'mi': 1609.34, 'yd': 0.9144, 'ft': 0.3048, 'inch': 0.0254,
        'km': 1000, 'm': 1, 'cm': 0.01, 'mm': 0.001
    }
    units = {
        "Nautical Miles": 'nmi', "Miles": 'mi', "Yards": 'yd', "Feet": 'ft', 
        "Inches": 'inch', "Kilometers": 'km', "Meters": 'm', "Centimeters": 'cm', 
        "Millimeters": 'mm'
    }

    def convert_length(amt, from_unit, to_unit):
        """
        Convert the length from one unit to another based on the conversion factors.
        """
        # Invariant: Assert that the from_unit and to_unit are valid
        assert from_unit in factors, f"Invalid from_unit: {from_unit}"
        assert to_unit in factors, f"Invalid to_unit: {to_unit}"
        
        # Invariant: Assert that the amount is a valid number and non-negative
        assert isinstance(amt, (int, float)), f"Amount should be a number, got {type(amt)}"
        assert amt >= 0, f"Amount must be non-negative, got {amt}"

        if from_unit != 'm':
            amt = amt * factors[from_unit]
        return amt / factors[to_unit]

    def update_result(*args):
        """
        Callback to update the result field when inputs or units change.
        """
        try:
            amt = float(input_field.get())
            # Invariant: Ensure the amount is non-negative
            assert amt >= 0, f"Amount must be a non-negative number, got {amt}"
        except ValueError:
            result_field.set('Invalid input')
            return
        except AssertionError as e:
            result_field.set(str(e))
            return

        from_unit = input_unit.get()
        to_unit = output_unit.get()

        # Invariant: Ensure that both units are selected and valid
        assert from_unit != 'Select Unit', "From Unit must be selected"
        assert to_unit != 'Select Unit', "To Unit must be selected"

        result = convert_length(amt, units[from_unit], units[to_unit])
        result_field.set(f"{result:.4f}")

    # Create the main window
    root = Toplevel()
    root.title("Length Converter")

    # Create the frame for the UI elements
    main_frame = ttk.Frame(root, padding="3 3 12 12")
    main_frame.pack(fill=BOTH, expand=1)

    # Title label
    title_label = Label(main_frame, text="Length Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    title_label.grid(column=1, row=1)

    # Variables for input and output
    input_amount = StringVar()
    input_amount.set('0')
    result_field = StringVar()

    input_unit = StringVar()
    output_unit = StringVar()
    input_unit.set('Select Unit')
    output_unit.set('Select Unit')

    # Input field for amount
    input_field = ttk.Entry(main_frame, width=20, textvariable=input_amount)
    input_field.grid(row=1, column=2, sticky=(W, E))

    # Dropdown menu for input unit
    input_unit_menu = OptionMenu(main_frame, input_unit, *units.keys())
    input_unit_menu.grid(column=3, row=1, sticky=W)

    # Output field for conversion result
    ttk.Entry(main_frame, textvariable=result_field, state="readonly").grid(column=2, row=3, sticky=(W, E))

    # Dropdown menu for output unit
    output_unit_menu = OptionMenu(main_frame, output_unit, *units.keys())
    output_unit_menu.grid(column=3, row=3, sticky=W)

    # Bind input field and unit menus to update result
    input_field.bind('<KeyRelease>', update_result)
    input_unit.trace("w", update_result)
    output_unit.trace("w", update_result)

    # Adjust padding for all child widgets
    for child in main_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Focus on the input field
    input_field.focus()

    root.mainloop()