import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import tempfile

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)

def create_jar():
    folder = folder_var.get()
    jar_name = jar_name_var.get().strip()
    main_class = main_class_var.get().strip()

    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    if not jar_name:
        messagebox.showerror("Error", "Please enter a name for the JAR file.")
        return

    if not jar_name.endswith(".jar"):
        jar_name += ".jar"

    jar_path = filedialog.asksaveasfilename(
        defaultextension=".jar",
        filetypes=[("JAR files", "*.jar")],
        initialfile=jar_name
    )

    if not jar_path:
        return

    # Create temporary MANIFEST.MF if main class is provided
    manifest_file = None
    if main_class:
        manifest_content = f"Manifest-Version: 1.0\nMain-Class: {main_class}\n"
        manifest_dir = tempfile.mkdtemp()
        manifest_file = os.path.join(manifest_dir, "MANIFEST.MF")
        with open(manifest_file, "w") as f:
            f.write(manifest_content)

    try:
        if manifest_file:
            subprocess.run(
                ["jar", "cmf", manifest_file, jar_path, "-C", folder, "."],
                check=True
            )
        else:
            subprocess.run(
                ["jar", "cf", jar_path, "-C", folder, "."],
                check=True
            )
        messagebox.showinfo("Success", f"JAR file created:\n{jar_path}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to create JAR file. Is Java installed and `jar` in PATH?")

# GUI setup
root = tk.Tk()
root.title("JAR File Creator with Main-Class Support")

folder_var = tk.StringVar()
jar_name_var = tk.StringVar(value="myapp.jar")
main_class_var = tk.StringVar()

tk.Label(root, text="Select folder containing .class files:").pack(pady=5)
tk.Entry(root, textvariable=folder_var, width=50).pack()
tk.Button(root, text="Browse", command=select_folder).pack(pady=5)

tk.Label(root, text="Enter JAR file name:").pack(pady=5)
tk.Entry(root, textvariable=jar_name_var, width=30).pack()

tk.Label(root, text="(Optional) Main-Class (e.g., com.example.Main):").pack(pady=5)
tk.Entry(root, textvariable=main_class_var, width=40).pack()

tk.Button(root, text="Create JAR", command=create_jar, bg="green", fg="white").pack(pady=10)

root.mainloop()
