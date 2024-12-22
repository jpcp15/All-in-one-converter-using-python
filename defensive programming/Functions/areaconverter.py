import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk

def AreaConverter():
    # Create the main window
    wind = Toplevel()
    wind.minsize(width=400, height=150)
    wind.maxsize(width=400, height=150)

    # Conversion factors for various area units (in square meters)
    meter_factors = {
        'square meter': 1, 'square km': 1000000, 'square rood': 1011.7141056, 'square cm': 0.0001,
        'square foot': 0.09290304, 'square inch': 0.00064516, 'square mile': 2589988.110336, 
        'millimeter': 0.000001, 'square rod': 25.29285264, 'square yard': 0.83612736, 
        'square township': 93239571.9721, 'square acre': 4046.8564224, 'square are': 100, 
        'square barn': 1e-28, 'square hectare': 10000, 'square homestead': 647497.027584
    }

    # Assert that all units in the meter_factors are positive and non-zero
    for unit, factor in meter_factors.items():
        assert factor > 0, f"Conversion factor for {unit} must be positive"

    def convert_area(x, from_unit, to_unit):
        """
        Convert the area from one unit to another based on the conversion factors.
        """
        # Invariant: from_unit and to_unit must be valid keys in meter_factors
        assert from_unit in meter_factors, f"Invalid from_unit: {from_unit}"
        assert to_unit in meter_factors, f"Invalid to_unit: {to_unit}"

        # Assert that the amount is a valid number
        assert isinstance(x, (int, float)), f"Amount should be a number, got {type(x)}"

        # Perform the conversion
        result = (float(x) * meter_factors[from_unit]) / meter_factors[to_unit]
        return result

    def update_conversion_result(*args):
        """
        Callback to update the result field when inputs change.
        """
        try:
            amt = float(area_input.get())
            # Assert that the amount is a non-negative number
            assert amt >= 0, "Amount must be a non-negative number"
        except ValueError:
            result_output.delete(0, END)
            result_output.insert(0, 'Invalid input')
            return
        except AssertionError as e:
            result_output.delete(0, END)
            result_output.insert(0, str(e))
            return

        from_unit = from_var.get()
        to_unit = to_var.get()

        # Invariant: ensure the user has selected valid units
        assert from_unit != 'From Unit', "From Unit must be selected"
        assert to_unit != 'To Unit', "To Unit must be selected"

        result = convert_area(amt, from_unit, to_unit)
        if result is not None:
            result_output.delete(0, END)
            result_output.insert(0, f"{result:.4f}")
        else:
            result_output.delete(0, END)
            result_output.insert(0, 'Conversion error')

    # Title label
    title_label = Label(wind, text="Area Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    title_label.grid(column=1, row=1)

    # Input field for amount
    area_input = Entry(wind)
    area_input.grid(row=1, column=2)

    # List of available units
    unit_values = list(meter_factors.keys())

    # Variables for input and output units
    from_var = StringVar(wind)
    to_var = StringVar(wind)
    from_var.set('From Unit')
    to_var.set('To Unit')

    # Dropdown menu for selecting "from" unit
    from_option = OptionMenu(wind, from_var, *unit_values)
    from_option.grid(row=1, column=3)

    # Dropdown menu for selecting "to" unit
    to_option = OptionMenu(wind, to_var, *unit_values)
    to_option.grid(row=3, column=3)

    # Output field for conversion result
    result_output = Entry(wind)
    result_output.grid(row=3, column=2)

    # Bind the conversion function to update the result whenever the input or units change
    area_input.bind('<KeyRelease>', update_conversion_result)
    from_var.trace("w", update_conversion_result)
    to_var.trace("w", update_conversion_result)

    wind.mainloop()
    