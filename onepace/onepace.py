import sys
import re
import os
from time import sleep
from alive_progress import alive_it
from pathlib import Path

def get_relevant_folders(orig_path: Path, keyword: str, all_folders: list[str]) -> list[Path]:
    return [
        orig_path / folder_path for folder_path in all_folders if \
            folder_path.startswith('[One Pace]') and keyword in folder_path
    ]

def move_files(abs_paths: list[Path], dest: Path, arc_key: str):
    print("Moving files...")
    sleep(1)
    pattern = re.compile(r'{} (\d+)'.format(re.escape(arc_key)))
    iterator = alive_it(abs_paths)
    for folder in iterator:
        files = [folder / file for file in os.listdir(folder)] # abs paths
        for file in files:
            group = pattern.findall(file.name)
            if not group or len(group) > 1:
                print(f'Problem with file in path:\n{file}')
                continue

            number = group[0]
            new_name = f'{arc_key} - {number}.mkv'
            new_path = dest / new_name

            os.rename(file.as_posix(), new_path.as_posix())

def remove_folders(abs_paths: list[Path]):
    print("Removing old files...")
    sleep(1)
    iterator = alive_it(abs_paths)
    for folder in iterator:
        os.rmdir(folder.as_posix())

    print("ARIGATOOOOO")

def onepace(orig_path: Path, onepace_path: Path, arc_key: str):
    all_folders = os.listdir(orig_path)
    print("Getting relevant files...")
    relevant_folders = get_relevant_folders(orig_path, arc_key, all_folders)
    sleep(2)

    if not relevant_folders:
        print(f"No folders found for {name}")
        sys.exit(1)
    
    onepace_path.mkdir(exist_ok=True)
    arc_path = onepace_path / arc_key
    arc_path.mkdir(exist_ok=True)

    move_files(relevant_folders, arc_path, arc_key)
    remove_folders(relevant_folders)