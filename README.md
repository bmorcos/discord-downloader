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
usage: downloader.py [-h] [-ft FILETYPES [FILETYPES ...]] [-o OUTPUT_DIR]
                     [-c CHANNELS [CHANNELS ...]] [-s SERVER]
                     [-n NUM_MESSAGES] [-d] [-v] [-p] [-a AFTER] [-b BEFORE]
                     [-z] [-fs FILTER_STR]
                     token

Download files and attachments from Discord!

positional arguments:
  token                 API token for your discord bot.

optional arguments:
  -h, --help            show this help message and exit
  -ft FILETYPES [FILETYPES ...], --filetypes FILETYPES [FILETYPES ...]
                        List of filetypes you want downloaded, e.g. 'txt',
                        'png'. Default is all filetypes. Specify multiple
                        items as so: -c 'first' 'second'.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Path to where files are saved locally. A new directory
                        will be made in the given 'output_dir'. Defaults to
                        the current working directory.
  -c CHANNELS [CHANNELS ...], --channels CHANNELS [CHANNELS ...]
                        List of channels in which to search for files. Default
                        is all channels. Specify multiple items as so: -c
                        'first' 'second'.
  -s SERVER, --server SERVER
                        Name of the server in which to search for files.
                        Default is the first server in the client list.
  -n NUM_MESSAGES, --num_messages NUM_MESSAGES
                        How many messages into channel history to search for
                        files. Pass 0 for no limit.
  -d, --dry_run         Don't actually download files, recommended to use with
                        '-v'.
  -v, --verbose         Show every file found.
  -p, --prepend_user    Prepend name of user who uploaded the file to the
                        local filename.
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
  -z, --zipped          Zip all downloaded files into an archive and delete
                        them.
  -fs FILTER_STR, --filter_str FILTER_STR
                        Only save files that contain the given string.

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


