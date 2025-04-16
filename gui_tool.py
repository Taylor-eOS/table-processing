import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import openpyxl

def filter_csv(input_file, output_file, postnr_list, hovedbranche_list):
    if input_file.lower().endswith('.xlsx'):
        df = pd.read_excel(input_file, dtype=str)
    else:
        df = pd.read_csv(input_file, dtype=str)
    if postnr_list:
        df = df[df["Postnr."].isin(postnr_list)]
    if hovedbranche_list:
        pattern = "|".join(hovedbranche_list)
        df = df[df["Hovedbranche"].str.contains(pattern, na=False, case=False, regex=True)]
    df.to_csv(output_file, index=False)

class FilterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CVR Filter")
        self.input_file = ""
        self.postnr_values = []
        self.hovedbranche_values = []
        tk.Label(root, text="").grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        tk.Label(root, text="Postnr.").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(root, text="Hovedbranche").grid(row=1, column=1, padx=5, pady=5)
        self.list_postnr = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False, width=30, height=10)
        self.list_postnr.grid(row=2, column=0, padx=5, pady=5)
        self.list_hovedbranche = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=False, width=40, height=10)
        self.list_hovedbranche.grid(row=2, column=1, padx=5, pady=5)
        self.btn_load = tk.Button(root, text="Open File", command=self.load_options)
        self.btn_load.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.btn_filter_save = tk.Button(root, text="Save", command=self.filter_and_save)
        self.btn_filter_save.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

    def load_options(self):
        if not self.input_file:
            path = filedialog.askopenfilename(
                filetypes=[("CSV or Excel files", "*.csv *.xlsx"), ("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
            )
            if not path:
                return
            self.input_file = path
        try:
            if self.input_file.lower().endswith('.xlsx'):
                df = pd.read_excel(self.input_file, dtype=str)
            else:
                df = pd.read_csv(self.input_file, dtype=str)
            if "Postnr." not in df.columns or "Hovedbranche" not in df.columns:
                messagebox.showerror("Error", "Input file must contain 'Postnr.' and 'Hovedbranche' columns.")
                return
            self.postnr_values = sorted(df["Postnr."].dropna().unique().tolist())
            self.hovedbranche_values = sorted(df["Hovedbranche"].dropna().unique().tolist())
            self.list_postnr.delete(0, tk.END)
            for item in self.postnr_values:
                self.list_postnr.insert(tk.END, item)
            self.list_hovedbranche.delete(0, tk.END)
            for item in self.hovedbranche_values:
                self.list_hovedbranche.insert(tk.END, item)
            messagebox.showinfo("Loaded", f"Loaded {len(self.postnr_values)} Postnr. and {len(self.hovedbranche_values)} Hovedbranche options.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def filter_and_save(self):
        if not self.input_file:
            messagebox.showerror("Error", "No input file selected.")
            return
        selected_postnr = [self.postnr_values[int(i)] for i in self.list_postnr.curselection()] if self.postnr_values else []
        selected_hovedbranche = [self.hovedbranche_values[int(i)] for i in self.list_hovedbranche.curselection()] if self.hovedbranche_values else []
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not output_file:
            return
        try:
            filter_csv(self.input_file, output_file, selected_postnr, selected_hovedbranche)
            messagebox.showinfo("Success", "Filtered CSV saved.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FilterGUI(root)
    root.mainloop()

