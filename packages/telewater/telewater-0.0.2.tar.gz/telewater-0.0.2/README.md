# telewater

A telegram bot that applies watermark on images, gifs and videos.


## Requirements

Make sure to have these installed in your system.

- [python3.9+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) (the bot is built with the telethon library)
- [ffmpeg](https://ffmpeg.org/) (used by the bot for applying watermark)

### Verification

Open you terminal to check if you have all basic requirements properly installed.

1. Run `python --version` and you should get something like this `Python 3.9.2` (or above).
2. Run `pip --version` and you should get `pip 20.2.2` (or above).

    > Some systems may require to use `python3` and `pip3` instead of the above.

3. Run `ffmpeg -h` and it should display a help message and version above `4.2.4`.

## Installation

```shell
pip install telewater
```


## Configuration

Create a file named `.env` inside your current directory (or the directory from which you desire to run the `telewater` command.)

Fill the file with your `API_ID` and `API_HASH`

Example:

```txt
API_ID=12345
API_HASH=102837:kjfjfk9r9JOIJOIjoi_jf9wr0w
```

Replace the above values with the actual values. Learn [how to get them](https://docs.telethon.dev/en/latest/basic/signing-in.html) for your telegram account.


## Run

Simply run `telewater` command from your terminal.


