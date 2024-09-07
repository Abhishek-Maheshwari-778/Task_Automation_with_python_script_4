import os
import shutil
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

# Setup logging
log_file = "file_organizer.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("Script started")

def organize_files(path, custom_folders=None, include_subdirectories=False):
    if custom_folders is None:
        custom_folders = {}

    if include_subdirectories:
        files = []
        for root, dirs, file_names in os.walk(path):
            for name in file_names:
                files.append(os.path.join(root, name))
    else:
        files = [os.path.join(path, file) for file in os.listdir(path)]
    
    for file in files:
        # Ignore hidden files
        if os.path.basename(file).startswith('.'):
            continue

        # Get the file extension
        _, extension = os.path.splitext(file)
        extension = extension[1:]  # Remove the dot

        # Skip if the file has no extension
        if not extension:
            continue

        # Determine target folder
        if extension in custom_folders:
            target_folder = os.path.join(path, custom_folders[extension])
        else:
            target_folder = os.path.join(path, extension)

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logging.info(f"Created directory: {target_folder}")

        # Handle filename conflicts
        base_name = os.path.basename(file)
        target_file = os.path.join(target_folder, base_name)

        counter = 1
        while os.path.exists(target_file):
            base_name_without_ext, ext = os.path.splitext(base_name)
            target_file = os.path.join(target_folder, f"{base_name_without_ext}_{counter}{ext}")
            counter += 1

        # Move the file
        shutil.move(file, target_file)
        logging.info(f"Moved {file} to {target_file}")

    logging.info("Script completed")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_path)

def start_organizing():
    path = entry_path.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid directory.")
        return

    custom_folders = {
        'jpg': 'Images',
        'png': 'Images',
        'mp3': 'Music',
        'pdf': 'Documents'
    }

    include_subdirs = subdir_var.get()

    try:
        organize_files(path, custom_folders=custom_folders, include_subdirectories=include_subdirs)
        messagebox.showinfo("Success", "Files organized successfully!")
    except Exception as e:
        logging.error(f"Error during file organization: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Setup GUI
root = tk.Tk()
root.title("File Organizer")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Path Selection
label_path = tk.Label(frame, text="Select Directory:")
label_path.grid(row=0, column=0, sticky="w")

entry_path = tk.Entry(frame, width=50)
entry_path.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(frame, text="Browse", command=browse_folder)
button_browse.grid(row=0, column=2, padx=5, pady=5)

# Subdirectory Option
subdir_var = tk.BooleanVar()
check_subdir = tk.Checkbutton(frame, text="Organize Subdirectories", variable=subdir_var)
check_subdir.grid(row=1, column=1, sticky="w", padx=5, pady=5)

# Start Button
button_start = tk.Button(frame, text="Start Organizing", command=start_organizing)
button_start.grid(row=2, column=1, pady=10)

root.mainloop()
