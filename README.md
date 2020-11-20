# Discord Downloader

A simple bot that will search channels in your server and bulk download files.
There are lots of option to help you restrict which channels are searched, what
files and file types are saved, in what date ranges to search, etc. It will even
zip them up for you.


## Getting Started

This repo only has one requirement:

```
pip install discord
```

But first you will need to create a bot and invite it to your server. The
[discord.py docs](https://discordpy.readthedocs.io/en/latest/discord.html) have
great instructions for this. **Make sure your bot has permission to read message
history**.


## Usage

I recommend taking a look through some of the options first:
```
$ python downloader.py --help
usage: downloader.py [-h] [-a AFTER] [-b BEFORE] [-c CHANNELS [CHANNELS ...]]
                     [-d] [-es EXCLUDE_STR] [-ft FILETYPES [FILETYPES ...]]
                     [-is INCLUDE_STR] [-n NUM_MESSAGES] [-o OUTPUT_DIR] [-p]
                     [-s SERVER] [-v] [-z]
                     token

Download files and attachments from Discord!

positional arguments:
  token                 API token for your discord bot.

optional arguments:
  -h, --help            show this help message and exit
  -a AFTER, --after AFTER
                        Search 'num_messages' starting at this date moving
                        forward unless 'before' was also provided, in which
                        case all files are searched between the given dates.
                        Provide date as a str 'yyyy-mm-dd.
  -b BEFORE, --before BEFORE
                        Search 'num_messages' starting at this date moving
                        backwards unless 'after' was also provided, in which
                        case all files are searched between the given dates.
                        Provide date as a str 'yyyy-mm-dd.
  -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                        List of channels in which to search for files. Default
                        is all channels. Specify multiple items as so: -c
                        'first' 'second'.
  -d, --dry_run         Don't actually download files, recommended to use with
                        '-v'.
  -es EXCLUDE_STR, --exclude_str EXCLUDE_STR
                        Only save files that do not contain the given string.
  -ft FILETYPES [FILETYPES ...], --filetypes FILETYPES [FILETYPES ...]
                        List of filetypes you want downloaded, e.g. 'txt',
                        'png'. Default is all filetypes. Specify multiple
                        items as so: -c 'first' 'second'.
  -is INCLUDE_STR, --include_str INCLUDE_STR
                        Only save files that contain the given string.
  -n NUM_MESSAGES, --num_messages NUM_MESSAGES
                        How many messages into channel history to search for
                        files. Note this is messages, not files! you may get
                        zero files. Pass 0 for no limit, default is 200.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to where files are saved locally. A new directory
                        will be made in the given 'output_dir'. Defaults to
                        the current working directory.
  -p, --prepend_user    Prepend name of user who uploaded the file to the
                        local filename.
  -s SERVER, --server SERVER
                        Name of the server in which to search for files.
                        Default is the first server in the client list.
  -v, --verbose         Show every file found.
  -z, --zipped          Zip all downloaded files into an archive and delete
                        them.

```

and doing dry runs or verbose dry runs before downloading ( ``-v, -d``):

```
python downloader.py $DISCORD_TOKEN -v -d
```

That being said the defaults are fairly reasonable, the bot will search the the
most recent 200 messages in each channel for files and download them to the
current directory:

```
python downloader.py $DISCORD_TOKEN
```

where ``$DISCORD_TOKEN`` is the bot token found on your discord developer page.


