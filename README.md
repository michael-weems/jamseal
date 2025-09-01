# Jam Seal

Prep and upload audio files and artifacts from jam sessions.

## Problem Statement

I'm recording music / jam-sessions on a regular basis, and need a tool to quickly take all the finished assets and upload them to my various storage drives. I'm just writing this for my needs so I'm not trying to make it the most flexible tool.

I need it to support copying files to:
- an external harddrive
- Google Drive (I have Google Drive sync mapped to a folder in my external harddrive)
- my nfs NAS

## Usage

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
