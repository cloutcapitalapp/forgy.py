# forgy.py

A python script that organizes large (Or small) file systems by automatically sorting files into appropriate folders based on their types, bringing order to chaotic directories.

## Features

- **Automatic File Organization**: Sorts files into categorized folders based on their extensions
- **Misc Folders Management**: Consolidates miscellaneous folders into a single location
- **Detailed Reports**: Generates comprehensive reports including:
  - Organization timestamp
  - Drive space information
  - Number of files moved by category
  - Total size of organized content
  - List of unorganized files

## Supported File Categories

- Images (.jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg, .ico)
- Documents (.pdf, .doc, .docx, .txt, .xlsx, .csv, .ppt, .pptx, .rtf, .odt)
- Videos (.mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .3gp)
- Audio (.mp3, .wav, .flac, .m4a, .aac, .wma, .ogg, .midi, .mid)
- Compressed Files (.zip, .rar, .7z, .tar, .gz, .bz2, .xz, .iso)
- Executables (.exe, .msi, .app, .dmg, .pkg, .deb, .rpm)
- Code Files (.py, .java, .cpp, .h, .js, .html, .css, .php, .sql)

## Requirements

- Python 3.x
- tkinter (usually comes with Python)
- psutil (`pip install psutil`)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/cloutcapitalapp/forgy.py.git
cd forgy.py
```

2. Install required packages:
```bash
pip install psutil
```

3. Run the script:
```bash
python forgy.py
```

## Usage

1. Launch the application
2. Click "Browse" to select the directory you want to organize
3. Choose one of two organization options:
   - **Organize Files**: Sorts files into category-based folders
   - **Organize Misc Folders**: Moves miscellaneous folders into a single container folder

## Report Generation

After each organization operation, the application automatically generates a detailed report containing:
- Timestamp of the organization
- Type of operation performed
- Directory path
- Drive information (total, used, and free space)
- Number of files moved per category
- Total size of organized content
- List of any unorganized files

Reports are saved in the selected directory with the naming format: `organization_report_YYYYMMDD_HHMMSS.txt`

## Safety Features

- Original directory structure is preserved
- Protected folders (category folders and misc_folders) are never moved
- Error handling for file operations
- Read-only display of selected path
- Drive space information before organization

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

[MIT License](LICENSE)

## Author

[cloutcapitalapp](https://github.com/cloutcapitalapp)
