import os
import argparse
import json
import fnmatch
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any

def is_text_file(file_path: str, sample_size: int = 8192) -> bool:
    """Determine if a file is text by examining its content."""
    try:
        with open(file_path, 'rb') as f:
            return b'\x00' not in f.read(sample_size)
    except IOError:
        return False

def normalize_content(content: str) -> str:
    """Normalize line endings to Unix-style (LF)."""
    return content.replace('\r\n', '\n').replace('\r', '\n')

def get_file_info(file_path: str, base_path: str, include_content: bool = True, max_size: int = 10*1024*1024) -> Dict[str, Any]:
    """Get information about a file."""
    rel_path = os.path.relpath(file_path, base_path).replace(os.sep, '/')
    file_info = {"path": rel_path}

    if include_content:
        try:
            with open(file_path, 'rb') as f:
                content = f.read(max_size)
                if is_text_file(file_path):
                    decoded_content = content.decode('utf-8', errors='replace')
                    file_info["content"] = normalize_content(decoded_content)
                else:
                    file_info["content"] = "<binary_content>"
        except Exception as e:
            file_info["error"] = str(e)

    return file_info

def generate_snapshot(input_dir: str, ignore_patterns: List[str], include_content: bool, max_size: int) -> Dict[str, Any]:
    """Generate a snapshot of the directory."""
    snapshot = {
        "files": []
    }

    script_name = os.path.basename(__file__)
    output_name = "directory_snapshot.json"  # Default output name

    for root, dirs, files in os.walk(input_dir):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        
        for file in files:
            if any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns):
                continue
            
            # Explicitly check for the script and output file
            if file == script_name or file == output_name:
                continue
            
            file_path = os.path.join(root, file)
            try:
                file_info = get_file_info(file_path, input_dir, include_content, max_size)
                snapshot["files"].append(file_info)
            except Exception as e:
                # If there were no errors before, initialize the errors list
                if "errors" not in snapshot:
                    snapshot["errors"] = []
                snapshot["errors"].append({
                    "path": os.path.relpath(file_path, input_dir).replace(os.sep, '/'),
                    "error": str(e)
                })

    return snapshot

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a directory snapshot for LLM analysis.")
    parser.add_argument("-i", "--input", default=".", help="Input directory (default: current directory)")
    parser.add_argument("-o", "--output", default="directory_snapshot.json", help="Output JSON file name")
    parser.add_argument("--ignore", nargs='+', default=['.git', 'node_modules', '*.pyc', '__pycache__', '*.log', 'target', 'Cargo.lock'], 
                        help="Patterns of files/folders to ignore (supports wildcards)")
    parser.add_argument("--max-size", type=int, default=1024*1024, help="Maximum file size to include content, in bytes (default: 1MB)")
    parser.add_argument("--no-content", action="store_true", help="Exclude file contents from the snapshot")
    
    args = parser.parse_args()

    # Generate the snapshot
    start_time = time.time()
    snapshot = generate_snapshot(args.input, args.ignore, not args.no_content, args.max_size)
    
    # Write the snapshot to a JSON file
    with open(args.output, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    # Print summary information
    end_time = time.time()
    print(f"Snapshot generated in {end_time - start_time:.2f} seconds.")
    print(f"Total files processed: {len(snapshot['files'])}")
    if 'errors' in snapshot:
        print(f"Errors encountered: {len(snapshot['errors'])}")
    print(f"Output written to: {args.output}")

if __name__ == "__main__":
    main()