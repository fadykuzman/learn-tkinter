import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
import csv


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, label='', input_class=ttk.Entry,
        input_var=None, input_args=None, label_args=None,
        **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var
        if input_class in (ttk.Checkbutton, ttk.Button,
        ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(
                self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W, tk.E))
            input_args["textvariable"] = input_var
        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E, tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton,
        ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.deselect('1.0', tk.END)
            self.input.insert('1.0', value)
        else: # input must be an ENtry-type widget with no variable
            self.input.delete(0, tk.END)
            self.input.insert(0, value)

class DataRecordForm(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}
        self.reset()
        
        wrapped_function = self.register(self.has_five_or_less_chars)
        vcmd = (wrapped_function, '%P')
        recordinfo = tk.LabelFrame(self,
            text="Record Information")
        
        self.inputs['Date'] = LabelInput(recordinfo, "Date",
            input_var= tk.StringVar(),
            input_args={'validate':'key',
            'validatecommand':vcmd})
        self.inputs['Date'].grid(row=0, column=0)

        self.inputs['Time'] = LabelInput(recordinfo, "Time",
            input_class=ttk.Combobox, input_var=tk.StringVar(),
            input_args={
                'values':['8:00', '12:00', '16:00','20:00']})
        self.inputs['Time'].grid(row=0, column=1)

        self.inputs['Technician'] = LabelInput(recordinfo,
            "Technician", input_var=tk.StringVar())
        self.inputs['Technician'].grid(row=0, column=2)
        recordinfo.grid(row=0, column=0)

        environmentinfo = tk.LabelFrame(self, 
            text="Environment Data")
        self.inputs['Humidity'] = LabelInput(environmentinfo,
            "Humidity (g/m³)",
            tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={
                'from_':0.5, 
                'to': 52.0, 
                'increment': .01})
        self.inputs['Humidity'].grid(row=0, column=0)
        self.inputs['Temperature'] = LabelInput(environmentinfo,
            "Temperature (C)",
            tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={
                'from_':4.0, 
                'to': 40.0, 
                'increment': .1})
        self.inputs['Temperature'].grid(row=0, column=1)
        self.inputs['Light'] = LabelInput(environmentinfo,
            "Light (klx)", tk.Spinbox,
            input_var=tk.IntVar(),
            input_args={'from_':0, 'to':100})
        self.inputs['Light'].grid(row=0, column=2)
        self.inputs['Equipment Fault'] = LabelInput(environmentinfo,
            'Equipment Fault',
            ttk.Checkbutton,
            input_var=tk.BooleanVar())
        self.inputs['Equipment Fault'].grid(
            row=1, column=0, columnspan=3)
        environmentinfo.grid(row=1, column=0)

        plantinfo = tk.LabelFrame(self, text="Plant Data")
        self.inputs['Plants'] = LabelInput(plantinfo,
            "Plants", tk.Spinbox, input_var=tk.IntVar(),
            input_args={'from_': 0, 'to': 20})
        self.inputs['Plants'].grid(row=0, column=0)
        self.inputs['Blossoms'] = LabelInput(plantinfo,
            'Blossoms', tk.Spinbox, input_var=tk.IntVar(),
            input_args={'from_': 0, 'to': 10000})
        self.inputs['Blossoms'].grid(row=0, column=1)
        self.inputs['Fruit'] = LabelInput(plantinfo,
            'Fruit', tk.Spinbox, input_var=tk.IntVar(),
            input_args={'from_': 0, 'to':1000})
        self.inputs['Fruit'].grid(row=0, column=2)
        self.inputs['Max. Height'] = LabelInput(plantinfo,
            'Max. Height', tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to':1000, 'increment': .1})
        self.inputs['Max. Height'].grid(row=0, column=3)
        self.inputs['Min. Height'] = LabelInput(plantinfo,
            'Min. Height', tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 1000, 'increment': .1})
        self.inputs['Min. Height'].grid(row=0, column=4)
        self.inputs['Median Height'] = LabelInput(plantinfo,
            'Median Height', tk.Spinbox, input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 1000, 'increment': .1})
        self.inputs['Median Height'].grid(row=0, column=5)
        plantinfo.grid(row=2, column=0)

        self.inputs['Notes'] = LabelInput(self,
            'Notes', tk.Text, input_args={'width': 75, 'height':10})
        self.inputs['Notes'].grid(sticky='w', row=3, column=0)
 
    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')
           
    def has_five_or_less_chars(string):
        return len(string) <= 5

class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('ABQ Data Entry Application')
        self.resizable(width=False, height=False)
        ttk.Label(self, text='ABQ Data Entry Application',
            font=('TkDefaultFont', 16)
        ).grid(row=0)
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10, pady=10)
        self.savebutton = ttk.Button(self, text='Save',
            command=self.on_save).grid(sticky=tk.E, row=2, padx=10)
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status
        ).grid(sticky=(tk.W, tk.E), row=3, padx=10)

    def on_save(self):
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = 'abq_data_record_{}.csv'.format(datestring)
        newfile = not os.path.exists(filename)
        data = self.recordform.get()
        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

if __name__ == '__main__':
    app = Application()
    app.mainloop()
