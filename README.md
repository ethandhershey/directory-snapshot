# Directory Snapshot Tool

## Overview

The Directory Snapshot Tool is a Python script that generates a comprehensive snapshot of a directory's structure and file contents. It's particularly useful for capturing project structures and content for analysis by Large Language Models (LLMs) or for quick project overviews.

## Features

- Captures directory structure and file contents in a single JSON file
- Configurable file size limit for content inclusion
- Ability to exclude file contents for large directories
- Customizable ignore patterns for excluding files and directories
- Automatic exclusion of binary files and handling of text encodings
- Efficient processing of large directories

## Installation

1. Ensure you have Python 3.6 or higher installed.
2. Clone this repository or download the `snapshot.py` script.

No additional dependencies are required.

## Usage

Basic usage:

```bash
python snapshot.py
```

This will create a snapshot of the current directory and save it as `directory_snapshot.json`.

### Command-line Options

```
usage: snapshot.py [-h] [-i INPUT] [-o OUTPUT] [--ignore IGNORE [IGNORE ...]]
                   [--max-size MAX_SIZE] [--no-content]

Generate a directory snapshot for LLM analysis.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory (default: current directory)
  -o OUTPUT, --output OUTPUT
                        Output JSON file name (default: directory_snapshot.json)
  --ignore IGNORE [IGNORE ...]
                        Patterns of files/folders to ignore (supports wildcards)
  -max-size MAX_SIZE    Maximum file size to include content, in bytes (default: 1MB)
  --no-content          Exclude file contents from the snapshot
```

### Examples

1. Snapshot a specific directory:
   ```bash
   python snapshot.py -i /path/to/your/project
   ```

2. Custom output file name:
   ```bash
   python snapshot.py -o project_snapshot.json
   ```

3. Ignore specific files or directories:
   ```bash
   python snapshot.py --ignore "*.log" "temp_*" ".vscode"
   ```

4. Increase the max file size for content inclusion:
   ```bash
   python snapshot.py --max-size 5242880  # 5MB
   ```

5. Generate a structure-only snapshot (no file contents):
   ```bash
   python snapshot.py --no-content
   ```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "files": [
    {
      "path": "relative/path/to/file",
      "content": "file contents (if included)"
    },
    // ... more files
  ],
  "errors": [
    {
      "path": "relative/path/to/problematic/file",
      "error": "Error message"
    },
    // ... any errors encountered (if any)
  ]
}
```

Note: The "errors" key will only be present if errors were encountered during the snapshot process.

## Use Cases

- Quickly capture project structure and contents for documentation
- Prepare project snapshots for analysis by AI models or code review tools
- Create lightweight backups of text-based projects
- Generate overviews of directory contents for archival purposes
