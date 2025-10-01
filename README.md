# Jam Seal

Prep and upload audio files and artifacts from jam sessions.

## Problem Statement

I'm recording music / jam-sessions on a regular basis, and need a tool to quickly take all the finished assets and upload them to my various storage drives. I'm just writing this for my needs so I'm not trying to make it the most flexible tool.

I need it to support copying files to:
- an external harddrive
- Google Drive (I have Google Drive sync mapped to a folder in my external harddrive)
- my nfs NAS

## Usage

### Configuration

Create a `config.toml` file in this workspace directory, formatted like below:

```toml
[drives]

[drives.a]
path = "/path/to/your/drive"
output_format = "wav"
include_project = true

[drives.b]
path = "/path/to/drive/b"
output_format = "flac"
include_project = false
```

#### Options

- `[drives.a]` specifies which drive the
- `path` --> full-path on the file-system to copy files to
- `output_format` --> `flac` | `wav` are supported currently
- `include_project` --> whether to also copy the logic-pro project to that location

#### Example

Example configuration:
```toml
[drives]

[drives.google]
path = "/mnt/gdrive"
output_format = "wav"
include_project = false

[drives.nas]
path = "/mnt/mynas/audio"
output_format = "flac"
include_project = true
```

### "Sealing" a project

Done with a jam, time to upload to storage: 

```zsh
./seal /path/to/your/project/dir # using the project dir, copy files into the storage locations
                                 # convert .wav --> .flac for google drive
                                 # creates new dir in these locations with the name of today's date

./seal /path/to/your/project/dir custom-name # same as above, but use a custom dir name
```

### "Un-sealing" a project

Want to do some more work on a past jam: 

```zsh
./unseal /path/to/your/storage/dir /path/to/new/local/project/dir # take the logicx project and "unseal" it to the desired local dir
```

### Convert all .wav files in dir to .flac

```zsh
./flacify /path/to/dir
```
