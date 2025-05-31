import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from agents.classifier_agent import ClassifierAgent
from memory.shared_memory import SharedMemory

class RedirectText:
    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self):
        pass  # Needed for file-like object interface

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Agent AI System")
        self.geometry("700x500")

        self.memory = SharedMemory()
        self.classifier = ClassifierAgent(self.memory)

        self.create_widgets()
        self.load_files()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Select input file:")
        self.label.pack(pady=5)

        self.file_combo = ttk.Combobox(self, state="readonly")
        self.file_combo.pack(fill='x', padx=10)

        self.process_btn = ttk.Button(self, text="Process File", command=self.process_file)
        self.process_btn.pack(pady=10)

        self.output = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.output.pack(expand=True, fill='both', padx=10, pady=10)

    def load_files(self):
        input_dir = "inputs"
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        self.file_combo['values'] = files
        if files:
            self.file_combo.current(0)

    def process_file(self):
        file_name = self.file_combo.get()
        if not file_name:
            messagebox.showwarning("Warning", "Please select a file.")
            return

        file_path = os.path.join("inputs", file_name)
        self.output.insert(tk.END, f"Processing {file_name}...\n")
        self.output.see(tk.END)

        # Redirect stdout to the Text widget
        old_stdout = sys.stdout
        sys.stdout = RedirectText(self.output)

        try:
            self.classifier.route(file_path)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Restore original stdout
            sys.stdout = old_stdout

        # Now show memory log too
        self.output.insert(tk.END, "\nMemory Log:\n")
        for row in self.memory.fetch_all():
            self.output.insert(tk.END, f"{row}\n")
        self.output.insert(tk.END, "-"*50 + "\n")
        self.output.see(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
