import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import sys
from datetime import datetime
import psutil

class FileOrganizerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Organizer")
        self.window.geometry("600x500")
        
        self.file_types = {
            'images': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'),
            'documents': ('.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv', '.ppt', '.pptx', '.rtf', '.odt'),
            'videos': ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp'),
            'audio': ('.mp3', '.wav', '.flac', '.m4a', '.aac', '.wma', '.ogg', '.midi', '.mid'),
            'compressed': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'),
            'executables': ('.exe', '.msi', '.app', '.dmg', '.pkg', '.deb', '.rpm'),
            'code': ('.py', '.java', '.cpp', '.h', '.js', '.html', '.css', '.php', '.sql')
        }
        
        self.setup_ui()

    def get_directory_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def get_drive_info(self, path):
        drive = psutil.disk_usage(path)
        return {
            'total': drive.total,
            'used': drive.used,
            'free': drive.free,
            'percent': drive.percent
        }

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    def generate_report(self, base_dir, operation_type, moved_items, unorganized_files=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(base_dir, f"organization_report_{timestamp}.txt")
        
        drive_info = self.get_drive_info(base_dir)
        
        with open(report_path, 'w') as report:
            report.write(f"File Organization Report\n")
            report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Operation Type: {operation_type}\n")
            report.write(f"Directory: {base_dir}\n\n")
            
            report.write("Drive Information:\n")
            report.write(f"Total Space: {self.format_size(drive_info['total'])}\n")
            report.write(f"Used Space: {self.format_size(drive_info['used'])}\n")
            report.write(f"Free Space: {self.format_size(drive_info['free'])}\n")
            report.write(f"Usage: {drive_info['percent']}%\n\n")
            
            report.write("Organization Results:\n")
            if operation_type == "File Organization":
                for category, count in moved_items.items():
                    if count > 0:
                        category_path = os.path.join(base_dir, category)
                        category_size = self.get_directory_size(category_path)
                        report.write(f"{category.capitalize()}:\n")
                        report.write(f"  Files Moved: {count}\n")
                        report.write(f"  Total Size: {self.format_size(category_size)}\n")
                
                if unorganized_files:
                    report.write("\nUnorganized Files:\n")
                    for file in unorganized_files:
                        report.write(f"  - {file}\n")
            else:  # Misc Folders Organization
                report.write(f"Folders Moved to misc_folders: {moved_items}\n")
                misc_size = self.get_directory_size(os.path.join(base_dir, "misc_folders"))
                report.write(f"Total Size of misc_folders: {self.format_size(misc_size)}\n")

        return report_path

    def setup_ui(self):
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(fill=tk.X)
        
        tk.Label(frame, text="Selected Directory:").pack(anchor='w')
        
        self.path_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.path_var, state='readonly', width=50).pack(pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Organize Files", command=self.organize_files).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Organize Misc Folders", command=self.organize_misc_folders).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Text(self.window, height=15, width=50)
        self.status.pack(padx=20, pady=(0, 20))

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
    
    def organize_files(self):
        if not self.path_var.get():
            messagebox.showerror("Error", "Please select a directory first")
            return
        
        try:
            base_dir = self.path_var.get()
            moved_counts = {category: 0 for category in self.file_types}
            
            for folder in self.file_types:
                folder_path = os.path.join(base_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
            
            unorganized_files = []
            for filename in os.listdir(base_dir):
                file_path = os.path.join(base_dir, filename)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(filename)[1].lower()
                    file_moved = False
                    
                    for category, extensions in self.file_types.items():
                        if ext in extensions:
                            destination = os.path.join(base_dir, category, filename)
                            shutil.move(file_path, destination)
                            moved_counts[category] += 1
                            file_moved = True
                            break
                    
                    if not file_moved:
                        unorganized_files.append(filename)
            
            # Generate and save report
            report_path = self.generate_report(base_dir, "File Organization", moved_counts, unorganized_files)
            
            # Update status
            self.status.delete(1.0, tk.END)
            self.status.insert(tk.END, "File organization complete!\n\n")
            for category, count in moved_counts.items():
                self.status.insert(tk.END, f"{category.capitalize()}: {count} files moved\n")
            
            if unorganized_files:
                self.status.insert(tk.END, "\nUnorganized files:\n")
                for file in unorganized_files:
                    self.status.insert(tk.END, f"- {file}\n")
            
            self.status.insert(tk.END, f"\nDetailed report saved to:\n{report_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def organize_misc_folders(self):
        if not self.path_var.get():
            messagebox.showerror("Error", "Please select a directory first")
            return
        
        try:
            base_dir = self.path_var.get()
            misc_folders_dir = os.path.join(base_dir, "misc_folders")
            os.makedirs(misc_folders_dir, exist_ok=True)
            
            moved_folders = 0
            protected_folders = set(list(self.file_types.keys()) + ['misc_folders'])
            
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path) and item not in protected_folders:
                    try:
                        new_path = os.path.join(misc_folders_dir, item)
                        shutil.move(item_path, new_path)
                        moved_folders += 1
                    except Exception as e:
                        self.status.insert(tk.END, f"Error moving {item}: {str(e)}\n")
            
            # Generate and save report
            report_path = self.generate_report(base_dir, "Misc Folders Organization", moved_folders)
            
            # Update status
            self.status.delete(1.0, tk.END)
            self.status.insert(tk.END, "Miscellaneous folders organization complete!\n\n")
            self.status.insert(tk.END, f"Number of folders moved to misc_folders: {moved_folders}\n")
            if moved_folders == 0:
                self.status.insert(tk.END, "\nNo miscellaneous folders found to organize.")
            
            self.status.insert(tk.END, f"\nDetailed report saved to:\n{report_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.run()
