import os
import sys
import subprocess
from enum import Enum
from datetime import datetime

import log
import tomllib


def defaults():
    now = datetime.now()
    _c = {
        "config_file": "config.toml",
        "date": now.strftime("%Y-%m-%d"),
        "input": "",
        "dry": False,
        "verbose": False,
    }
    return _c

config = defaults()

print(sys.argv)

argc = len(sys.argv)
i = 0
while i < argc:
    if sys.argv[i] == "-verbose":
        log._verbose = True
        config["verbose"] = True
    i = i + 1

i = 1
while i < argc:
    if sys.argv[i] == "-config":
        i = i + 1
        config["config_file"] = sys.argv[i]
        log.verbose(f"[arg] config-file: {config["config_file"]}")
    elif sys.argv[i] == "-verbose":
        log.verbose(f"[arg] verbose: {config["verbose"]}")
    elif sys.argv[i] == "-dry":
        config["dry"] = True
        log.verbose(f"[arg] dry: {config["dry"]}")
    elif sys.argv[i] == "-date":
        i = i + 1
        config["date"] = sys.argv[i]
        log.verbose(f"[arg] date: {config["date"]}")
    else:
        config["input"] = sys.argv[i]
        log.verbose(f"[arg] input: {config["input"]}")

    i = i + 1

if not config["config_file"]:
    log.fail("no config file specified")
    sys.exit(1)

try:
    log.verbose(f"read config from: {config["config_file"]}")
    with open(config["config_file"], "rb") as f:
        config_file = tomllib.load(f)
except:
    log.fail(f"read config file: {config["config_file"]}")
    sys.exit(1)

if not config["input"]:
    log.fail("no input directory specified")
    sys.exit(1)


log._verbose=config["verbose"]
dry=config["dry"]
input_dir=config["input"]
out = config["date"]

log.verbose(f"{log.BLUE}use >>{log.RESET} VERBOSE={log._verbose}")
log.verbose(f"{log.BLUE}use >>{log.RESET} DRY={dry}")
log.verbose(f"{log.BLUE}use >>{log.RESET} INPUT_DIR={input_dir}")

DRIVE_PATH = "path"

class FileAction(Enum):
    Copy = "copy"
    Compress = "compress"
    Ffmpeg = "ffmpeg"

ACTION = "action"
FFMPEG_OPTS = "ffmpeg_opts"
FFMPEG_FORMAT = "ffmpeg_format"

out_dir= config["date"]

try:
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        log.verbose(f"{log.BLUE}{filename} >>{log.RESET} path={file_path}")

        base_name, extension = os.path.splitext(file_path)
        extension = extension[1:]
        name=os.path.basename(file_path)
        new_name=name.replace(' ', '_')

        log.verbose(f"{log.BLUE}{filename} >>{log.RESET} name={name}")
        log.verbose(f"{log.BLUE}{filename} >>{log.RESET} base_name={base_name}")
        log.verbose(f"{log.BLUE}{filename} >>{log.RESET} new_name={new_name}")

        for key in config_file["drives"]:
            log.verbose(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key}{log.RESET}")
            drive = config_file["drives"][key]

            if drive.get(extension) is None:
                log.warn(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} unsupported file extension: {extension}")
                log.verbose(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} skip file")
                continue

            file_actions = drive[extension]
            full_out_dir=os.path.join(drive[DRIVE_PATH], out_dir)
            os.makedirs(full_out_dir, exist_ok=True)

            out_base_filename = os.path.join(full_out_dir, new_name)
            log.verbose(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} action={file_actions[ACTION]}")
            log.verbose(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} out_base_filename={out_base_filename}")

            cmd = []
            if file_actions[ACTION] == FileAction.Compress.value:
                cmd = ["zip", "-9", "-r", f"{out_base_filename}.zip", file_path]
            elif file_actions[ACTION] == FileAction.Ffmpeg.value:
                if file_actions.get(FFMPEG_OPTS) is None:
                    log.fail(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} no ffmpeg opts specified: {file_actions[FFMPEG_OPTS]}")
                    continue

                ffmpeg_args = file_actions[FFMPEG_OPTS].split(" ")

                out_base_name, in_extension = os.path.splitext(out_base_filename)

                cmd = ["ffmpeg", "-i", file_path, *ffmpeg_args, f"{out_base_name}.{file_actions[FFMPEG_FORMAT]}"]
            elif file_actions[ACTION] == FileAction.Copy.value:
                cmd = ["cp", "-r", file_path, f"{out_base_filename}"]
            else:
                log.fail(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} no cmd specified")
                continue

            log.verbose(f"{log.BLUE}{filename} >>{log.RESET} {log.YELLOW}{key} >>{log.RESET} cmd={cmd}")

            if dry:
                log.done(f"dry run: {cmd}")
            else:
                log.verbose(cmd)
                subprocess.run(cmd)

except FileNotFoundError as e:
    log.fail(f"file not found: {e}")
except Exception as e:
    log.fail(f"unknown error: {e}")
