import os
import shutil
import argparse
from datetime import datetime

def create_backup(src_path):
    base_dir = os.path.dirname(src_path.rstrip("/\\"))
    project_name = os.path.basename(src_path.rstrip("/\\"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder_name = f"{project_name}_backup_{timestamp}"
    backup_path = os.path.join(base_dir, backup_folder_name)

    print(f"[+] Backing up project to: {backup_path}")
    shutil.copytree(src_path, backup_path)
    print("[✓] Backup complete.\n")
    return backup_path

def map_project_structure(root_path, prefix="", output_text=None, output_md=None):
    entries = sorted(os.listdir(root_path))
    entries_count = len(entries)
    
    for idx, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        is_last = idx == entries_count - 1

        connector = "└── " if is_last else "├── "
        line = prefix + connector + entry

        if output_text:
            output_text.write(line + "\n")

        if output_md:
            output_md.write(f"{prefix}{connector}**{entry}**\n")
        
        print(line)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            map_project_structure(path, prefix + extension, output_text, output_md)

if __name__ == "__main__":
    try:
        
        project_path = input("Enter the full path to your project (e.g., C:/root/myproject): ").strip()
        project_path = os.path.abspath(project_path)

        if not os.path.exists(project_path):
            print(f"[!] Error: The path does not exist: {project_path}")
        else:
            print(f"[~] Scanning project: {project_path}")

            create_backup(project_path)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_file_name = f"project_structure_{timestamp}.txt"
            md_file_name = f"project_structure_{timestamp}.md"

            with open(text_file_name, "w", encoding="utf-8") as text_file, open(md_file_name, "w", encoding="utf-8") as md_file:
                
                md_file.write(f"# Project Structure for {os.path.basename(project_path)}\n\n")

                print("\n📁 Generating project structure in text and markdown formats...\n")
                map_project_structure(project_path, output_text=text_file, output_md=md_file)

            print(f"\n[✔] Project structure saved to: {text_file_name} and {md_file_name}")

    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

    input("\n[✔] Done. Press Enter to exit...")
