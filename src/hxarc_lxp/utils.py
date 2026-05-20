# -*- coding: utf-8 -*-

import contextlib
import csv
import json
import logging
from pathlib import Path
import sys
from typing import Any, Union
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


def get_contents(filepath: str) -> dict | list | None:
    fp = Path(filepath)
    if not fp.exists() or not fp.is_file():
        logger.error(f"input({filepath} not file or not file.")
        return None

    if fp.suffix == ".json":
        with fp.open(mode="r", encoding="ISO-8859-1") as fh:
            contents = json.load(fh)
        return contents

    elif fp.suffix == ".csv":
        incsv = []
        with fp.open(mode="r", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, dialect="excel")
            for row in reader:
                incsv.append(row)
        return incsv

    elif fp.suffix == ".tsv":
        intsv = []
        with fp.open(mode="r", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh, dialect="excel-tab")
            for row in reader:
                intsv.append(row)
        return intsv

    elif fp.suffix == ".srt":
        with fp.open(mode="r", encoding="utf-8-sig") as fh:
            rows = fh.readlines()
        return rows

    else:
        logger.error(f"can't read file format({fp.suffix})")
        return None


def save_file(
    data: list[dict[str, Any]],
    filename: str,
    folder: str,
    overwrite: bool = True,
) -> bool:
    """saves a list of dicts as filename extension dictates: json or csv."""
    extension = Path(filename).suffix
    if extension not in (".json", ".csv"):
        logger.error(f"unknown format({extension}); accepts json or csv")
        return False

    filepath = Path(folder) / filename
    if filepath.exists():
        if not overwrite:
            logger.error(f"path({filepath}) exists, not overwriting")
            return False
        else:
            logger.warning(f"overwriting path({filepath})!!!!")

    if extension == ".json":
        filepath.write_text(json.dumps(data, indent=4))

    elif extension == ".csv":
        with filepath.open(mode="w", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    logger.info(f"done writing data to file({filepath}) as format({extension})")
    return True


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


# from http://stackoverflow.com/a/29824059
# accepts stdin as filename "-"
@contextlib.contextmanager
def _smart_open(filename, mode="r"):
    if filename == "-":
        if mode is None or mode == "" or "r" in mode:
            fhandle = sys.stdin
        else:
            fhandle = sys.stdout
    else:
        fhandle = open(filename, mode)

    try:
        yield fhandle
    finally:
        if filename != "-":
            fhandle.close()


def secToHMS(time: Union[float, int]) -> str:
    """Converts from seconds to hh:mm:ss format"""
    # Round it to an integer.
    time = int(round(float(time), 0))

    # Downconvert through hours.
    seconds = int(time % 60)
    time -= seconds
    minutes = int((time / 60) % 60)
    time -= minutes * 60
    hours = int((time / 3600) % 24)

    # Make sure we get enough zeroes.
    if int(seconds) == 0:
        seconds = "00"
    elif int(seconds) < 10:
        seconds = "0" + str(seconds)
    if int(minutes) == 0:
        minutes = "00"
    elif int(minutes) < 10:
        minutes = "0" + str(minutes)
    if int(hours) == 0:
        hours = "00"
    if int(hours) < 10:
        hours = "0" + str(hours)

    # Send back a string
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


def describeLinkData(newlink: dict) -> dict:
    """Adds notes to links based on file type, like (image link) or (PDF file)."""
    image_types = [
        ".png",
        ".gif",
        ".jpg",
        ".jpeg",
        ".svg",
        ".tiff",
        ".tif",
        ".bmp",
        ".jp2",
        ".jif",
        ".pict",
        ".webp",
    ]

    if newlink["href"].endswith(tuple(image_types)):
        newlink["text"] += " (image link)"
    if newlink["href"].endswith(".pdf"):
        newlink["text"] += " (PDF file)"
    if newlink["href"].endswith(".ps"):
        newlink["text"] += " (PostScript file)"
    if newlink["href"].endswith(".zip"):
        newlink["text"] += " (zip file)"
    if newlink["href"].endswith(".tar.gz"):
        newlink["text"] += " (tarred gzip file)"
    if newlink["href"].endswith(".gz"):
        newlink["text"] += " (gzip file)"
    return newlink
