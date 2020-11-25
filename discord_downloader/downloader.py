import os
import shutil
import datetime
import discord

from discord_downloader.config import cfg
from discord_downloader.parser import base_parser
from discord_downloader.utils import (
    none_or_int,
    none_or_str,
    none_or_date,
    none_or_list,
)


def main(
    client,
    token,
    filetypes=none_or_str(cfg.get("args", "filetypes")),
    output_dir=str(cfg.get("args", "output_dir")),
    channels=none_or_list(cfg.get("args", "channels")),
    server=none_or_str(cfg.get("args", "server")),
    dry_run=cfg.getboolean("args", "dry_run"),
    num_messages=none_or_int(cfg.get("args", "num_messages")),
    verbose=cfg.getboolean("args", "verbose"),
    prepend_user=cfg.getboolean("args", "prepend_user"),
    after=none_or_date(cfg.get("args", "after")),
    before=none_or_date(cfg.get("args", "before")),
    zipped=cfg.getboolean("args", "zipped"),
    include_str=none_or_str(cfg.get("args", "include_str")),
    exclude_str=none_or_str(cfg.get("args", "exclude_str")),
):
    """Bot to download some files from discord

    See parser help strings for details
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

        if (after is not None and before is not None) or (
            num_messages is None or num_messages <= 0
        ):
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

    parser = base_parser
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
