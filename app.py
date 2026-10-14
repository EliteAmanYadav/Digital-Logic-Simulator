
import tkinter as tk
from tkinter import ttk, messagebox
from itertools import product


class DigitalLogicSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Logic Circuit Simulator")
        self.root.geometry("720x650")
        self.root.minsize(600, 550)

        self.q = 0
        self.input_vars = {}

        self.circuits = {
            "AND Gate": ["A", "B"],
            "OR Gate": ["A", "B"],
            "NOT Gate": ["A"],
            "NAND Gate": ["A", "B"],
            "NOR Gate": ["A", "B"],
            "XOR Gate": ["A", "B"],
            "XNOR Gate": ["A", "B"],
            "Half Adder": ["A", "B"],
            "Full Adder": ["A", "B", "Cin"],
            "2:1 Multiplexer": ["I0", "I1", "S"],
            "D Flip-Flop": ["D"],
        }

        self.build_ui()
        self.load_circuit()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="DIGITAL LOGIC CIRCUIT SIMULATOR",
            font=("Arial", 17, "bold")
        )
        title.pack(pady=18)

        ttk.Label(
            self.root,
            text="Select a circuit:"
        ).pack()

        self.circuit_var = tk.StringVar(value="AND Gate")

        self.circuit_box = ttk.Combobox(
            self.root,
            textvariable=self.circuit_var,
            values=list(self.circuits.keys()),
            state="readonly",
            width=28
        )
        self.circuit_box.pack(pady=8)
        self.circuit_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_circuit()
        )

        self.input_frame = ttk.LabelFrame(
            self.root,
            text="Binary Inputs",
            padding=15
        )
        self.input_frame.pack(fill="x", padx=35, pady=12)

        self.output_frame = ttk.LabelFrame(
            self.root,
            text="Circuit Output",
            padding=15
        )
        self.output_frame.pack(fill="x", padx=35, pady=10)

        self.result_var = tk.StringVar(
            value="Select a circuit and enter its inputs."
        )

        ttk.Label(
            self.output_frame,
            textvariable=self.result_var,
            font=("Consolas", 13, "bold"),
            justify="left"
        ).pack(anchor="w")

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=18)

        ttk.Button(
            self.button_frame,
            text="Evaluate Circuit",
            command=self.evaluate
        ).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            self.button_frame,
            text="Clock Pulse",
            command=self.clock_pulse
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            self.button_frame,
            text="Reset Flip-Flop",
            command=self.reset_flip_flop
        ).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(
            self.button_frame,
            text="Show Truth Table",
            command=self.show_truth_table
        ).grid(row=1, column=0, columnspan=3, pady=7)

        ttk.Label(
            self.root,
            text="ECE + CS Project | Python and Tkinter",
            foreground="gray"
        ).pack(side="bottom", pady=12)

    def load_circuit(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.input_vars.clear()
        circuit = self.circuit_var.get()

        for row, name in enumerate(self.circuits[circuit]):
            ttk.Label(
                self.input_frame,
                text=f"{name}:"
            ).grid(row=row, column=0, padx=15, pady=7, sticky="w")

            var = tk.StringVar(value="0")
            self.input_vars[name] = var

            ttk.Combobox(
                self.input_frame,
                textvariable=var,
                values=["0", "1"],
                state="readonly",
                width=8
            ).grid(row=row, column=1, padx=15, pady=7)

        if circuit == "D Flip-Flop":
            self.result_var.set(
                f"Current state: Q={self.q}, Qbar={1-self.q}\n"
                "Choose D, then press Clock Pulse to store it."
            )
        else:
            self.result_var.set("Enter inputs and click Evaluate Circuit.")

    def get_inputs(self):
        return {
            name: int(var.get())
            for name, var in self.input_vars.items()
        }

    def calculate(self, circuit, x):
        a = x.get("A", 0)
        b = x.get("B", 0)
        cin = x.get("Cin", 0)

        if circuit == "AND Gate":
            return {"Y": a & b}
        if circuit == "OR Gate":
            return {"Y": a | b}
        if circuit == "NOT Gate":
            return {"Y": 1 - a}
        if circuit == "NAND Gate":
            return {"Y": 1 - (a & b)}
        if circuit == "NOR Gate":
            return {"Y": 1 - (a | b)}
        if circuit == "XOR Gate":
            return {"Y": a ^ b}
        if circuit == "XNOR Gate":
            return {"Y": 1 - (a ^ b)}

        if circuit == "Half Adder":
            return {
                "Sum": a ^ b,
                "Carry": a & b
            }

        if circuit == "Full Adder":
            return {
                "Sum": a ^ b ^ cin,
                "Carry": (a & b) | (b & cin) | (a & cin)
            }

        if circuit == "2:1 Multiplexer":
            return {
                "Y": x["I0"] if x["S"] == 0 else x["I1"]
            }

        return {}

    def evaluate(self):
        circuit = self.circuit_var.get()

        if circuit == "D Flip-Flop":
            self.result_var.set(
                "D Flip-Flop is edge-triggered.\n"
                "Press Clock Pulse to capture D."
            )
            return

        inputs = self.get_inputs()
        outputs = self.calculate(circuit, inputs)

        input_text = ", ".join(
            f"{key}={value}" for key, value in inputs.items()
        )
        output_text = ", ".join(
            f"{key}={value}" for key, value in outputs.items()
        )

        self.result_var.set(
            f"Inputs: {input_text}\nOutputs: {output_text}"
        )

    def clock_pulse(self):
        if self.circuit_var.get() != "D Flip-Flop":
            messagebox.showinfo(
                "Clock Pulse",
                "Select D Flip-Flop to use the clock."
            )
            return

        d = self.get_inputs()["D"]
        self.q = d

        self.result_var.set(
            f"Clock rising edge detected!\n"
            f"D = {d}\nQ = {self.q}\nQbar = {1-self.q}"
        )

    def reset_flip_flop(self):
        self.q = 0

        if self.circuit_var.get() == "D Flip-Flop":
            self.result_var.set(
                "Flip-flop reset.\nQ = 0\nQbar = 1"
            )
        else:
            messagebox.showinfo(
                "Reset",
                "The flip-flop state has been reset to 0."
            )

    def show_truth_table(self):
        circuit = self.circuit_var.get()

        if circuit == "D Flip-Flop":
            messagebox.showinfo(
                "Truth Table",
                "D Flip-Flop stores D on a rising clock edge.\n"
                "Q(next) = D; without a clock edge, Q holds its state."
            )
            return

        names = self.circuits[circuit]
        window = tk.Toplevel(self.root)
        window.title(f"{circuit} - Truth Table")
        window.geometry("430x400")

        ttk.Label(
            window,
            text=f"Truth Table: {circuit}",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        table = ttk.Treeview(window, show="headings")
        table.pack(fill="both", expand=True, padx=15, pady=10)

        output_names = list(
            self.calculate(
                circuit, {name: 0 for name in names}
            ).keys()
        )

        columns = names + output_names
        table["columns"] = columns

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=75, anchor="center")

        for values in product([0, 1], repeat=len(names)):
            inputs = dict(zip(names, values))
            outputs = self.calculate(circuit, inputs)
            row = list(values) + list(outputs.values())
            table.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalLogicSimulator(root)
    root.mainloop()
