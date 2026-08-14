#!/usr/bin/env python3
"""Pin SideStore 0.6.3's em_proxy fetcher to its compatible legacy assets."""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FETCH_SCRIPT = REPOSITORY_ROOT / "Dependencies" / "em_proxy" / "fetch-prebuilt.sh"


def replace_once(contents: str, old: str, new: str) -> str:
    occurrences = contents.count(old)
    if occurrences != 1:
        raise RuntimeError(
            f"Expected exactly one matching block in {FETCH_SCRIPT}, found {occurrences}. "
            "The pinned em_proxy fetcher may have changed."
        )
    return contents.replace(old, new)


def main() -> None:
    contents = FETCH_SCRIPT.read_text(encoding="utf-8")
    contents = replace_once(
        contents,
        "    LATEST_COMMIT=`curl https://api.github.com/repos/SideStore/$1/releases/latest | "
        "perl -n -e '/Commit: https:\\\\/\\\\/github\\\\.com\\\\/[^\\\\/]*\\\\/[^\\\\/]*\\\\/commit\\\\/([^\"]*)/ && print $1'`",
        '    LATEST_COMMIT="49dc35b29779c7d9cf2529a2f2116c90d181fd19"',
    )
    latest_asset_url = "https://github.com/SideStore/$1/releases/latest/download/"
    pinned_asset_url = "https://github.com/SideStore/$1/releases/download/build/"
    occurrences = contents.count(latest_asset_url)
    if occurrences != 4:
        raise RuntimeError(
            f"Expected four legacy asset URLs in {FETCH_SCRIPT}, found {occurrences}."
        )
    contents = contents.replace(latest_asset_url, pinned_asset_url)
    FETCH_SCRIPT.write_text(contents, encoding="utf-8")
    print("Pinned SideStore 0.6.3 em_proxy downloads to the compatible build release.")


if __name__ == "__main__":
    main()
