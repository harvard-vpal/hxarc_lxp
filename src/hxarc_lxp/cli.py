# -*- coding: utf-8 -*-

"""Console script for hxarc_lxp."""

import logging
import sys
from pathlib import Path


import click

from hxarc_lxp.logs import config_log
from hxarc_lxp.hxarc_lxp import process_dir
from hxarc_lxp.utils import get_contents
from hxarc_lxp import vpal_version_comment as version_comment


# provide a file to log stuff, otherwise it's console only
# logfile = "{}/logs/cli.log".format(
#    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# )
# config_log(logfile=logfile)
config_log()
logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    "input_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, allow_dash=False),
)
@click.option(
    "--parjson",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
    help=(
        "filepath to json with input params,"
        'e.g. {"name": "value", "output_path": "/tmp/test"}'
    ),
)
# adds --version automagically!
@click.version_option(
    message="%(prog)s version %(version)s - " + version_comment,
    help="prints version and exits",
)
def cli(
    input_path: str,  # path to dir where export bundle was untarred
    parjson: str | None = None,  # remove if no other params
):
    """
    \b
    where INPUT_PATH is the dir created when export is untarred.
    \b
    If specifying output dir where to generate result files, stash it in the input
    json parjson as "output_path". If missing, cli assumes Path(input_path).parent
    In the example below, the resulting files will be created in /tmp/test.
    \b
    $> tar xvz --cd /tmp/test -f course.tgz
    $> ls -l /tmp/test/course  # course created when untarring
    total 8
    drwxr-xr-x@  12 nmaekawa  staff   384 Nov 20  2024 about/
    drwxr-xr-x@   3 nmaekawa  staff    96 Nov 20  2024 assets/
    drwxr-xr-x@   8 nmaekawa  staff   256 Nov 20  2024 chapter/
    drwxr-xr-x@   3 nmaekawa  staff    96 Nov 20  2024 course/
    -rw-r--r--@   1 nmaekawa  staff    58 Nov 20  2024 course.xml
    ...
    \b
    $> hxarc_lxp /tmp/test/course
    """

    # click.Path() already checked that this is a readable dir
    ipath = Path(input_path).resolve()  # absolute path
    for child in ipath.iterdir():
        if child.is_file() and child.name == "course.xml":
            logger.info(f"found course folder({child.parent})")

            # perhaps some validation before using the value cause it can be None
            # but if not None, it's a readable file
            contents = get_contents(parjson) if parjson else {}

            result = process_dir(child.parent, **contents)

            # can also pass params as dir, depending on how you func process_file wants
            # to handle params
            # result = process_file(child.parent, contents)

            logger.info(f"done! result is {result}")
            return 0

    logger.error(f"No course.xml file found in {ipath} -- NOTHING done")
    return 1  # return non-zero for errors that might be displayed to hxarc end user


if __name__ == "__main__":
    # return exit code from cli(), instead of main
    sys.exit(cli())  # pragma: no cover
