import os
import json
import argparse
from time import sleep
from pathlib import Path
from .onepace import onepace
from .download_onepace import download_onepace_json

def get_config_path(create=False):
    if os.name == 'posix':  # Linux or macOS
        settings_dir = os.path.expanduser('~/.config/onepace')
    elif os.name == 'nt':   # Windows
        settings_dir = os.path.join(os.getenv('APPDATA'), 'onepace')
    else:
        raise OSError('Unsupported operating system')

    settings_dir = Path(settings_dir)
    if create:
        settings_dir.mkdir(exist_ok=True, parents=True)
    settings_file = settings_dir / 'onepace.json'
    return settings_file

def check_initialized(func):
    def wrapper(*args, **kwargs):
        settings_file_path = get_config_path()
        if not settings_file_path.exists():
            print("please use init command first")
            return
        
        settings = load_settings()
        path = settings.get('path', None)
        if path is None or not os.path.exists(path):
            print("Configure file is corrupted. use init command")
            return
        
        kwargs['settings'] = settings
        return func(*args, **kwargs)
    return wrapper

def save_settings(settings):
    print('Saving...')
    sleep(2)
    settings_file = get_config_path()
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f'Configurations file saved in:\n{settings_file}\n\nTodoooooot\n')

def load_settings() -> dict:
    settings_file = get_config_path()
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {}

def init(*args, **kwargs):
    print("OKARISHIMASSSSS")
    path = Path(input('Enter path where torrent files are downloaded to: '))

    if not path.exists():
        answer = input("Path given doesn't exists.. create it?  y/n  ")
        if answer != 'y':
            print("Abroting... ")
            return
    
    os.makedirs(path, exist_ok=True)
    onepace_path = Path(path) / 'One Pace'

    settings = {'path': path.as_posix(), 'onepace_path': onepace_path.as_posix()}
    save_settings(settings)

@check_initialized
def fix_arc(*args, **kwargs):
    settings = kwargs['settings']
    args = kwargs['args']

    if settings is None:
        raise ValueError('settings not provided')
    downloads_path = settings.get('path')
    onepace_path = settings.get('onepace_path')
    
    onepace(Path(downloads_path), Path(onepace_path), args.arc)

def main():
    # Command-line argument parser
    parser = argparse.ArgumentParser(description='Your module description')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    # Initialization command
    init_parser = subparsers.add_parser('init', help='Initialize the module')
    init_parser.set_defaults(func=init)

    # Command requiring initialization
    command_parser = subparsers.add_parser('add-arc', help='move and rename episodes like a boss')
    command_parser.add_argument('arc', help='arc name capitalized')
    command_parser.set_defaults(func=fix_arc)

    download_json_parser = subparsers.add_parser('json', help='download the episodes json (takes a while)')
    download_json_parser.add_argument('path', help='json file path to save')
    download_json_parser.set_defaults(func=download_onepace_json)

    # Parse arguments and execute corresponding function
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args=args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()