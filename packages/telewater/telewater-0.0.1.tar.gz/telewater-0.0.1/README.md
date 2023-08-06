# watermark-gif-bot

A telegram bot that helps you apply an watermark image on GIFs.

**The following instructions assume that the reader is comfortable with the following tasks**

- using the terminal,
- cloning repositories using `git`,
- running `python` programs, and
- using bots/userbots made with the [Telethon](https://github.com/LonamiWebs/Telethon) library.


## Requirements

- [python3.9+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) (the bot is built with the telethon library)
- [ffmpeg](https://ffmpeg.org/) (used by the bot for applying watermark)
- [git](https://git-scm.com/) (for installing and updating this repo on your server)


## Installation

```shell

git clone https://github.com/aahniks/watermarker.git
cd watermarker

```


## Configuration

Create a file named `.env` inside the `watermarker` directory.

Fill the file with your `API_ID` and `API_HASH`

Example:

```txt
API_ID=12345
API_HASH=102837:kjfjfk9r9JOIJOIjoi_jf9wr0w
```

Replace the above values with the actual values. Learn [how to get them](https://docs.telethon.dev/en/latest/basic/signing-in.html) for your telegram account.


## Run

The `main.py` file is the entry point for running the bot. Run this module using the correct python version.
