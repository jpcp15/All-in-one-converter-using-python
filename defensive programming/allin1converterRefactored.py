import sys
import json
import tkinter as tk
from tkinter import *
import urllib.request
import webbrowser
from functools import partial
from tkinter import Tk, StringVar , ttk



###################################################################        
root = Tk()
root.title('ALL IN ONE CONVERTER')
root.geometry("450x400+100+200")
labelfont = ('Tahoma', 56, 'bold')
l=Label(root,text='ALL IN ONE CONVERTER',font = ("Tahoma", 20, "bold", "italic"), justify = CENTER)
l.place(x=70,y=10)

widget = Button(None, text="QUIT", bg="white", fg="red",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "red", overrelief = GROOVE, activebackground = "red", activeforeground="black", command=root.destroy).place(x=350,y=350)
#############################################################################################################################################

def CurrencyConverter():

    ids = {"US Dollar" : 'USD', "Euros" : 'EUR', "Indian Rupees" : 'INR', "Qatar Doha" : 'QAR', "Zimbwabe Harare" : 'ZWD', "Arab Emirates Dirham" : 'AED', "Pound Sterling" : 'GBP', "Japanese Yen" : 'JPY', "Yuan Renminbi" : 'CNY'}

def CurrencyConverter():
    # Currency IDs mapping
    ids = {
        "US Dollar": 'USD',
        "Euros": 'EUR',
        "Indian Rupees": 'INR',
        "Qatar Riyal": 'QAR',
        "Zimbabwe Dollar": 'ZWD',
        "Arab Emirates Dirham": 'AED',
        "Pound Sterling": 'GBP',
        "Japanese Yen": 'JPY',
        "Yuan Renminbi": 'CNY',
        "Philippine Peso": 'PHP'
    }

    # Fixer.io API key and endpoint
    API_KEY = "fffea497a4279524f01b786d728e59f6"  # Replace with your Fixer.io API key
    API_URL = f"http://data.fixer.io/api/latest?access_key=fffea497a4279524f01b786d728e59f6"

    def convert(amt, frm, to):
        try:
            # Assertions to validate that amount and currency codes are valid
            assert isinstance(amt, (int, float)), "Amount must be a number"
            assert amt >= 0, "Amount must be non-negative"
            assert frm in ids.values(), f"Invalid input currency code: {frm}"
            assert to in ids.values(), f"Invalid output currency code: {to}"

            # Fetch exchange rates
            response = urllib.request.urlopen(API_URL)
            data = json.loads(response.read().decode('utf-8'))

            # Check for API success
            if not data.get("success"):
                return f"Error: {data.get('error', {}).get('info', 'Unknown error')}"

            # Get conversion rates
            rates = data.get("rates", {})
            if frm not in rates or to not in rates:
                return "Currency not supported"

            # Perform the conversion
            rate_from = rates[frm]
            rate_to = rates[to]
            converted_amt = amt * (rate_to / rate_from)

            # Invariant: Converted amount should always be a positive number
            assert converted_amt >= 0, "Converted amount must be non-negative"

            return f"{converted_amt:.2f}"
        except AssertionError as ae:
            return f"Assertion Error: {str(ae)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def callback():
        try:
            amt = float(in_field.get())
            assert amt >= 0, "Amount must be non-negative"
        except ValueError:
            out_amt.set('Invalid input')
            return None
        except AssertionError as ae:
            out_amt.set(str(ae))
            return None

        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None
        else:
            frm = ids.get(in_unit.get())
            to = ids.get(out_unit.get())
            if frm and to:
                out_amt.set(convert(amt, frm, to))
            else:
                out_amt.set('Invalid currency selected')

    # Create Tkinter window
    root = Toplevel()
    root.title("Currency Converter")

    # Main frame
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.pack(fill=BOTH, expand=1)

    # Title label
    titleLabel = Label(mainframe, text="Currency Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    titleLabel.grid(column=1, row=1, columnspan=2)

    # Input/output variables
    in_amt = StringVar()
    in_amt.set('0')
    out_amt = StringVar()
    in_unit = StringVar()
    out_unit = StringVar()
    in_unit.set('Select Unit')
    out_unit.set('Select Unit')

    # Input field
    in_field = ttk.Entry(mainframe, width=30, textvariable=in_amt)
    in_field.grid(row=2, column=1, sticky=(W, E))

    # Input unit dropdown
    OptionMenu(mainframe, in_unit, *ids.keys()).grid(column=2, row=2, sticky=W)

    # Output field
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=1, row=4, sticky=(W, E))

    # Output unit dropdown
    OptionMenu(mainframe, out_unit, *ids.keys()).grid(column=2, row=4, sticky=W)

    # Calculate button
    ttk.Button(mainframe, text="Calculate", command=callback).grid(column=2, row=3, sticky=E)

    # Padding
    for child in mainframe.winfo_children():
        child.grid_configure(padx=20, pady=5)

    in_field.focus()
#################################################################################################

#################################################################################################

def WeightConverter():
    # Conversion factors to convert from units to grams (g)
    factors = {
        'kg': 1000, 'hg': 100, 'dg': 10, 'g': 1, 
        'deg': 0.1, 'cg': 0.01, 'mg': 0.001
    }

    # Dictionary mapping user-friendly names to factor keys
    unit_ids = {
        "Kilogram": 'kg', "Hectagram": 'hg', "Decagram": 'dg', 
        "Gram": 'g', "Decigram": 'deg', "Centigram": 'cg', "Milligram": 'mg'
    }

    def convert(amt, frm, to):
        """
        Convert the amount from one unit to another.
        Converts both to and from grams.
        """
        # Assertions for input validation
        assert isinstance(amt, (int, float)), "Amount must be a number"
        assert amt >= 0, "Amount must be non-negative"
        assert frm in factors, f"Invalid from unit: {frm}"
        assert to in factors, f"Invalid to unit: {to}"

        if frm == to:
            return amt  # No conversion needed if units are the same
        # Convert to grams first and then to the target unit
        amt_in_grams = amt * factors[frm]
        # Invariant: Conversion should result in a positive value
        result = amt_in_grams / factors[to]
        assert result >= 0, "Conversion result must be non-negative"
        return result

    def callback():
        """
        Handle the conversion logic when the user clicks the Calculate button.
        """
        try:
            amt = float(in_field.get())  # Get the input value
            assert amt >= 0, "Amount must be non-negative"
        except ValueError:
            out_amt.set('Invalid input')
            return None
        except AssertionError as ae:
            out_amt.set(str(ae))
            return None

        if in_unit.get() == 'Select Unit' or out_unit.get() == 'Select Unit':
            out_amt.set('Input or output unit not chosen')
            return None

        # Get the units from the dropdowns
        frm = unit_ids[in_unit.get()]
        to = unit_ids[out_unit.get()]

        # Perform the conversion
        try:
            result = convert(amt, frm, to)
            out_amt.set(f"{result:.4f}")  # Display the result with 4 decimal places
        except AssertionError as ae:
            out_amt.set(str(ae))

    # Initiate window
    root = Toplevel()
    root.title("Weight Converter")

    # Frame for content
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.pack(fill=BOTH, expand=1)

    titleLabel = Label(mainframe, text="Weight Converter", font=("tahoma", 12, "bold"), justify=CENTER)
    titleLabel.grid(column=1, row=1)

    # Variables to hold input and output values
    in_amt = StringVar(value='0')
    out_amt = StringVar()

    in_unit = StringVar(value='Select Unit')
    out_unit = StringVar(value='Select Unit')

    # Add input field for amount
    in_field = ttk.Entry(mainframe, width=20, textvariable=in_amt)
    in_field.grid(row=1, column=2, sticky=(W, E))

    # Add drop-down for input unit
    in_select = OptionMenu(mainframe, in_unit, *unit_ids.keys())
    in_select.grid(column=3, row=1, sticky=W)

    # Add output field and drop-down for output unit
    ttk.Entry(mainframe, textvariable=out_amt, state="readonly").grid(column=2, row=3, sticky=(W, E))
    out_select = OptionMenu(mainframe, out_unit, *unit_ids.keys())
    out_select.grid(column=3, row=3, sticky=W)

    # Add Calculate button
    calc_button = ttk.Button(mainframe, text="Calculate", command=callback)
    calc_button.grid(column=2, row=2, sticky=E)

    # Configure spacing for layout
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Focus on the input field initially
    in_field.focus()


    
###########################################################################################################
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


#############################################################################################################################################################

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


###################################################################################################################################################################


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


    

###################################################################################################################################################################################

#Links
def sensex(event):
    webbrowser.open_new(r"https://finance.yahoo.com/echarts?s=%5EBSESN")
def nifty(event):
    webbrowser.open_new(r"https://in.tradingview.com/symbols/NSE-NIFTY/")
def gold(event):
    webbrowser.open_new(r"https://www.kitco.com/price/precious-metals")
def silver(event):
    webbrowser.open_new(r"https://www.kitco.com/price/precious-metals")


####################################################################################
#Hovering
def color_config(widget, color, event):
    widget.configure(foreground=color)

text =Label(root, text="SENSEX",font = ("Courier", 14, "bold"))

text.bind("<Enter>", partial(color_config, text, "Green"))
text.bind("<Leave>", partial(color_config, text, "black"))
text.pack()
text.bind("<Button-1>",sensex)
text.place(x=350,y=120)
text =Label(root, text="NIFTY",font = ("Courier", 14, "bold"))

text.bind("<Enter>", partial(color_config, text, "green"))
text.bind("<Leave>", partial(color_config, text, "black"))
text.pack()
text.bind("<Button-1>",nifty)
text.place(x=350,y=150)

text =Label(root, text="GOLD",font = ("Courier", 14, "bold"))

text.bind("<Enter>", partial(color_config, text, "green"))
text.bind("<Leave>", partial(color_config, text, "black"))
text.pack()
text.bind("<Button-1>",gold)
text.place(x=350,y=180)

text =Label(root, text="SILVER",font = ("Courier", 14, "bold"))

text.bind("<Enter>", partial(color_config, text, "green"))
text.bind("<Leave>", partial(color_config, text, "black"))
text.pack()
text.bind("<Button-1>",silver)
text.place(x=350,y=210)
####################################################################################################
#TEMPERATURE CONVERTER
widget = Button(root, text="Temperature converter", bg="lightblue" , fg="green",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "green", overrelief = GROOVE, activebackground = "green", activeforeground="black", command=TemperatureConverter).place(x=50,y=120)
widget = Button(root, text="Length Converter", bg="lightblue" , fg="green",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "green", overrelief = GROOVE, activebackground = "green", activeforeground="black", command=LengthConverter).place(x=50,y=180)
widget = Button(root, text="Area Converter", bg="lightblue" , fg="green",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "green", overrelief = GROOVE, activebackground = "green", activeforeground="black", command=AreaConverter).place(x=50,y=240)
widget = Button(root, text="Currency converter", bg="lightblue" , fg="green",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "green", overrelief = GROOVE, activebackground = "green", activeforeground="black", command=CurrencyConverter).place(x=50,y=60)
widget = Button(root, text="Weight Converter", bg="lightblue" , fg="green",font = ("Tahoma", 14, "bold"), relief = RAISED, bd=5, justify = CENTER, highlightbackground = "green", overrelief = GROOVE, activebackground = "green", activeforeground="black", command=WeightConverter).place(x=50,y=300)

root.mainloop()