#!/usr/bin/env python3

import yaml
import argparse
import subprocess
from os import path


version = "0.1"


def load_config(config_file):
    scriptLocation = path.dirname(path.realpath(__file__))
    configLocation = path.join(scriptLocation, config_file)

    with open(configLocation, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Video file name")
    parser.add_argument("--version", action='version', version='v{}'.format(version), help="Shows script version")

    return parser.parse_args()
    

def get_file_path(fileArgument):
    if (path.isabs(fileArgument)):
        return fileArgument
    else:
        return path.join(path.abspath('.'), fileArgument)


args = init_parser()

moviePath = get_file_path(args.file)
subPath = path.splitext(moviePath)[0] + ".srt"

config = load_config("config.yml")
path2subify =config["subify"]

if not path.isfile(subPath):
    subCommand = f"{path2subify} dl \"{moviePath}\""
    subprocess.run(subCommand, shell=True)


movieCommand = f"mpv --fs \"{moviePath}\""
subprocess.run(movieCommand, shell=True)
