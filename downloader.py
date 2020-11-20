import os
import argparse
import datetime
import shutil
import discord


def main(
    client,
    token,
    filetypes=None,
    output_dir=os.getcwd(),
    channels=None,
    server=None,
    dry_run=False,
    num_messages=200,
    verbose=False,
    prepend_user=False,
    after=None,
    before=None,
    zipped=False,
    include_str=None,
    exclude_str=None,
):
    """Bot to download some files from discord

    See argparser below for parameter descriptions
    """

    download_dir = "discord_downloads_" + datetime.datetime.now().strftime("%Y%m%d")
    output_dir = os.path.join(output_dir, download_dir)
    os.makedirs(output_dir, exist_ok=True)

    @client.event
    async def on_ready(
        server=server,
        channels=channels,
        num_messages=num_messages,
        filetypes=filetypes,
        verbose=verbose,
        output_dir=output_dir,
        prepend_user=prepend_user,
        dry_run=dry_run,
        after=after,
        before=before,
        include_str=include_str,
        exclude_str=exclude_str,
    ):
        """Wait for client to be ready then do the thing

        Just doing everything inside here because I'm too lazy
        to deal with async
        """

        if server is None:
            server = client.guilds[0].name  # Default to first server

        if (after is not None and before is not None) or num_messages <= 0:
            num_messages = None  # Grab all files between dates, no limit

        # Instead of 'None', print 'inf' when searching unlimited messages
        num_str = str(num_messages) if num_messages is not None else "inf"

        app_info = await client.application_info()
        total = 0
        for g in client.guilds:
            if g.name == server:
                print(
                    f"Connected to {g.name} as {client.user},"
                    f" emissary of {app_info.owner.name}\n"
                )

                text_channels = g.text_channels
                for c in text_channels:
                    if channels is None or c.name in channels:
                        count = 0
                        if before is None and after is None:
                            print(
                                f"> Looking at last {num_str} messages"
                                f" in {c.name}..."
                            )
                        elif before is not None and after is not None:
                            print(
                                f"> Looking at all messages between {before:%Y-%m-%d}"
                                f" and {after:%Y-%m-%d} in {c.name}..."
                            )
                        elif before is not None:
                            print(
                                f"> Looking at last {num_str} before"
                                f" {before:%Y-%m-%d} messages in {c.name}..."
                            )
                        elif after is not None:
                            print(
                                f"> Looking at first {num_str} after"
                                f" {after:%Y-%m-%d} messages in {c.name}..."
                            )

                        async for m in c.history(
                            limit=num_messages, after=after, before=before
                        ):
                            for a in m.attachments:
                                if (
                                    (
                                        filetypes is None
                                        or a.filename.split(".")[-1] in filetypes
                                    )
                                    and (
                                        include_str is None or include_str in a.filename
                                    )
                                    and (
                                        exclude_str is None
                                        or exclude_str not in a.filename
                                    )
                                ):
                                    if verbose:
                                        print(f" > Found {a.filename}")
                                    count += 1
                                    fname = (
                                        m.author.name.replace(" ", "_")
                                        + "__"
                                        + a.filename
                                        if prepend_user
                                        else a.filename
                                    )
                                    fname = os.path.join(output_dir, fname)
                                    if not dry_run:
                                        await a.save(fname)

                        print(f" >> Found {count} files.")
                        total += count

        if dry_run:
            print(f"\n**** Dry run! 0 of {total} files saved!")
        else:
            print(f"\n**** Saved {total} files to {output_dir}")
        await client.logout()  #

    @client.event
    async def on_disconnect(zipped=zipped, dry_run=dry_run, output_dir=output_dir):
        """Print a logout message to confirm client exits"""
        if zipped and not dry_run:
            print("  ** Zipping and cleaning files...")
            shutil.make_archive(output_dir, "zip", output_dir)
            shutil.rmtree(output_dir)

        print("\nGoodbye world, be excellent to eachother!")

    client.run(token)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Download files and attachments from Discord!"
    )

    parser.add_argument("token", type=str, help="API token for your discord bot.")
    parser.add_argument(
        "-a",
        "--after",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help=(
            "Search 'num_messages' starting at this date moving forward "
            " unless 'before' was also provided, in which case"
            " all files are searched between the given dates."
            " Provide date as a str 'yyyy-mm-dd."
        ),
    )
    parser.add_argument(
        "-b",
        "--before",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help=(
            "Search 'num_messages' starting at this date moving backwards"
            " unless 'after' was also provided, in which case"
            " all files are searched between the given dates."
            " Provide date as a str 'yyyy-mm-dd."
        ),
    )
    parser.add_argument(
        "-c",
        "--channels",
        type=str,
        nargs="+",
        help=(
            "List of channels in which to search for files."
            " Default is all channels."
            " Specify multiple items as so: -c 'first' 'second'."
        ),
    )
    parser.add_argument(
        "-d",
        "--dry_run",
        action="store_true",
        help="Don't actually download files, recommended to use with '-v'.",
    )
    parser.add_argument(
        "-es",
        "--exclude_str",
        type=str,
        help="Only save files that do not contain the given string.",
    )
    parser.add_argument(
        "-ft",
        "--filetypes",
        type=str,
        nargs="+",
        help=(
            "List of filetypes you want downloaded, e.g. 'txt', 'png'."
            " Default is all filetypes."
            " Specify multiple items as so: -c 'first' 'second'."
        ),
    )
    parser.add_argument(
        "-is",
        "--include_str",
        type=str,
        help="Only save files that contain the given string.",
    )
    parser.add_argument(
        "-n",
        "--num_messages",
        type=int,
        default=200,
        help=(
            "How many messages into channel history to search for files."
            " Note this is messages, not files! you may get zero files."
            " Pass 0 for no limit, default is 200."
        ),
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=os.getcwd(),
        help=(
            "Path to where files are saved locally. A new directory will"
            " be made in the given 'output_dir'."
            " Defaults to the current working directory."
        ),
    )
    parser.add_argument(
        "-p",
        "--prepend_user",
        action="store_true",
        help="Prepend name of user who uploaded the file to the local filename.",
    )
    parser.add_argument(
        "-s",
        "--server",
        type=str,
        help=(
            "Name of the server in which to search for files."
            " Default is the first server in the client list."
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show every file found.",
    )
    parser.add_argument(
        "-z",
        "--zipped",
        action="store_true",
        help="Zip all downloaded files into an archive and delete them.",
    )

    args = parser.parse_args()

    client = discord.Client()

    main(
        client,
        args.token,
        filetypes=args.filetypes,
        output_dir=args.output_dir,
        channels=args.channels,
        server=args.server,
        dry_run=args.dry_run,
        num_messages=args.num_messages,
        verbose=args.verbose,
        prepend_user=args.prepend_user,
        after=args.after,
        before=args.before,
        zipped=args.zipped,
        include_str=args.include_str,
        exclude_str=args.exclude_str,
    )
