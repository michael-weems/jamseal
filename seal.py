import os
import subprocess

import log
import tomllib

with open("config.toml", "rb") as f:
    config_file = tomllib.load(f)

#ERROR="%F{red}err >>%f"
#DONE="%F{green}fin >>%f"

print(config_file)

def to_wav_cmd(in_file, out_file):
	return f"ffmpeg -i {in_file} -ar 44100 -c:a pcm_f32le {out_file}"

def to_flac_cmd(in_file, out_file):
	return f"ffmpeg -i {in_file} -c:a flac -compression_level 8 {out_file}"

def run_cmd(cmd):
    try:
        log.verbose(f"{cmd}")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("Cancelled")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with error: {e}")

# TODO: move these somewhere else + read in from cli args
log._verbose=True
dry=True
jam_dir="/home/"

log.verbose(f"{log.YELLOW}use >>{log.RESET} VERBOSE={log._verbose}")
log.verbose(f"{log.YELLOW}use >>{log.RESET} DRY={dry}")
log.verbose(f"{log.YELLOW}use >>{log.RESET} JAM_DIR={jam_dir}")

for key in config_file["drives"]:
    drive = config_file["drives"][key]

    log.verbose(f"{log.YELLOW}for >>{log.RESET} drive={key}")
    log.verbose(f"{log.YELLOW}  use >>{log.RESET} path={drive['path']}")
    log.verbose(f"{log.YELLOW}  use >>{log.RESET} format={drive['output_format']}")
    log.verbose(f"{log.YELLOW}  use >>{log.RESET} project={drive['include_project']}")



