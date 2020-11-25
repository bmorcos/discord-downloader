import argparse

from discord_downloader import cfg
from discord_downloader.utils import (
    none_or_int,
    none_or_str,
    none_or_date,
    none_or_list,
)


base_parser = argparse.ArgumentParser(
    description="Download files and attachments from Discord!"
)

base_parser.add_argument("token", type=str, help="API token for your discord bot.")
base_parser.add_argument(
    "-a",
    "--after",
    default=cfg.get("args", "after"),
    type=none_or_date,
    help=(
        "Search 'num_messages' starting at this date moving forward "
        " unless 'before' was also provided, in which case"
        " all files are searched between the given dates."
        " Provide date as a str 'yyyy-mm-dd'."
    ),
)
base_parser.add_argument(
    "-b",
    "--before",
    default=cfg.get("args", "before"),
    type=none_or_date,
    help=(
        "Search 'num_messages' starting at this date moving backwards"
        " unless 'after' was also provided, in which case"
        " all files are searched between the given dates."
        " Provide date as a str 'yyyy-mm-dd'."
    ),
)
base_parser.add_argument(
    "-c",
    "--channels",
    default=cfg.get("args", "channels"),
    type=none_or_list,
    nargs="+",
    help=(
        "List of channels in which to search for files."
        " Default is all channels."
        " Specify multiple items as so: -c 'first' 'second'."
    ),
)
base_parser.add_argument(
    "-d",
    "--dry_run",
    default=cfg.getboolean("args", "dry_run"),
    action="store_true",
    help="Don't actually download files, recommended to use with '-v'.",
)
base_parser.add_argument(
    "-es",
    "--exclude_str",
    default=cfg.get("args", "exclude_str"),
    type=none_or_str,
    help="Only save files that do not contain the given string.",
)
base_parser.add_argument(
    "-ft",
    "--filetypes",
    default=cfg.get("args", "filetypes"),
    type=none_or_str,
    nargs="+",
    help=(
        "List of filetypes you want downloaded, e.g. 'txt', 'png'."
        " Default is all filetypes."
        " Specify multiple items as so: -c 'first' 'second'."
    ),
)
base_parser.add_argument(
    "-is",
    "--include_str",
    default=cfg.get("args", "include_str"),
    type=none_or_str,
    help="Only save files that contain the given string.",
)
base_parser.add_argument(
    "-n",
    "--num_messages",
    default=cfg.get("args", "num_messages"),
    type=none_or_int,
    help=(
        "How many messages into channel history to search for files."
        " Note this is messages, not files! you may get zero files."
        " Pass 'None' for no limit, default is 200."
    ),
)
base_parser.add_argument(
    "-o",
    "--output_dir",
    default=cfg.get("args", "output_dir"),
    type=str,
    help=(
        "Path to where files are saved locally. A new directory will"
        " be made in the given 'output_dir'."
        " Defaults to the current working directory."
    ),
)
base_parser.add_argument(
    "-p",
    "--prepend_user",
    default=cfg.getboolean("args", "prepend_user"),
    action="store_true",
    help="Prepend name of user who uploaded the file to the local filename.",
)
base_parser.add_argument(
    "-s",
    "--server",
    default=cfg.get("args", "server"),
    type=none_or_str,
    help=(
        "Name of the server in which to search for files."
        " Default is the first server in the client list."
    ),
)
base_parser.add_argument(
    "-v",
    "--verbose",
    default=cfg.getboolean("args", "verbose"),
    action="store_true",
    help="Show every file found.",
)
base_parser.add_argument(
    "-z",
    "--zipped",
    default=cfg.getboolean("args", "zipped"),
    action="store_true",
    help="Zip all downloaded files into an archive and delete them.",
)
