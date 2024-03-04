import sys
import re
import os
from glob import glob
from alive_progress import alive_it
from pathlib import Path

ORIG = Path('D:\\TL Downloads\\TV Shows')

def get_relevant_folders(keyword: str, all_folders: list[str]) -> list:
    return [
        folder_path for folder_path in all_folders if \
            folder_path.startswith('[One Pace]' and keyword in folder_path)
    ]

def get_download_path() -> Path:
    pass

def get_onepace_path() -> Path:
    pass

def move_files(abs_paths: list[Path], dest: Path):
    pass

def onepace(orig_path: str):
    pass

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python3 copy_files.py <destination>")
        sys.exit(1)
    
    name = args[0]
    dest = ORIG / "One Pace" / name

    pattern = r'\[One Pace\]\[(\d+-\d+)\] {} (\d+) \[\d{3,4}p\]\[[A-F0-9]+\]'.format(re.escape(name))

    folders = [{'path': f, 'match': re.match(pattern, f)}  for f in os.listdir(ORIG) if re.match(pattern, f)]
    
    if not folders:
        print(f"No folders found for {name}")
        sys.exit(1)

    if not dest.exists():
        dest.mkdir()

    # move the mkv files to the destination
    iterator = alive_it(folders)
    for items in iterator:
        files = os.listdir((ORIG / items['path']).as_posix())
        _, number = items['match'].groups()
        new_name = f'{name} - {number}.mkv'

        if len(files) != 1:
            continue

        os.rename((ORIG / items['path'] / files[0]).as_posix(), (dest / new_name).as_posix())

    # delete the empty folders
    for items in folders:
        os.rmdir((ORIG / items['path']).as_posix())

    print(f"Moved {len(folders)} files to {dest}")
    print("Enjoy")