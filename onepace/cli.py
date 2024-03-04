import os
import json
import argparse
from pathlib import Path
from .onepace import onepace

if os.name == 'posix':  # Linux or macOS
    SETTINGS_DIR = os.path.expanduser('~/.config/onepace')
elif os.name == 'nt':   # Windows
    SETTINGS_DIR = os.path.join(os.getenv('APPDATA'), 'onepace')
else:
    raise OSError('Unsupported operating system')

# Ensure the settings directory exists
os.makedirs(SETTINGS_DIR, exist_ok=True)

SETTINGS_FILE: Path = Path(os.path.join(SETTINGS_DIR, 'onepace.json'))

def check_initialized(func):
    def wrapper(*args, **kwargs):
        if not SETTINGS_FILE.exists():
            print("please use init command first")
            return
        
        settings = load_settings()
        path = settings.get('path', None)
        if path is None or not os.path.exists(path):
            print("Configure file is corrupted. use init command")
            return
        
        return func(settings=settings)
    return wrapper

# Function to save settings
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Function to load settings
def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def init(*args, **kwargs):
    print("OKARISHIMASSSSS")
    path = input('Enter path where torrent files are downloaded to: ')

    if not os.path.exists(path):
        answer = input("Path given doesn't exists.. create it?  y/n  ")
        if answer != 'y':
            print("Abroting... ")
            return
    
    os.makedirs(path, exist_ok=True)
    settings = {'path': path}  # Example, you can add more settings here
    save_settings(settings)

    print(f'Configurations file saved in:\n{SETTINGS_FILE}\nTodoooooot')

@check_initialized
def fix_arc(settings):
    if settings is None:
        raise ValueError('settings not provided')
    downloads_path = settings.get('path')
    # onepace(downloads_path)
    print(f'hello!!')


def main():
    # Command-line argument parser
    parser = argparse.ArgumentParser(description='Your module description')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Initialization command
    init_parser = subparsers.add_parser('init', help='Initialize the module')
    # init_parser.add_argument('path', help='Path argument for initialization')
    init_parser.set_defaults(func=init)

    # Command requiring initialization
    command_parser = subparsers.add_parser('command', help='Your command')

    # Associate function with the command
    command_parser.set_defaults(func=fix_arc)

    # Parse arguments and execute corresponding function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()