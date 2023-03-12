## utdemofinder

**[Download Latest (.exe)](https://github.com/jack-avery/utdemofinder/releases/latest/download/utdemofinder.exe)**

**utdemofinder** is a utility program for the video game servers **Uncletopia** for **Team Fortress 2** to provide a simple user interface for moderators to search for SourceTV demos for specific users, including games played with other users.

![utdemofinder](https://cdn.discordapp.com/attachments/989252507102511124/1084584578871730317/image.png)

## Usage
1. Download and open **utdemofinder.exe**.
2. Insert a valid SteamID64 into the Steam ID64 box.
> This normally looks something like `76561198027298961`<br/>
> You can find this by opening the users' profile on Steam.<br/>
> If they have a vanity URL, [SteamRep Checker](https://addons.mozilla.org/en-CA/firefox/addon/steamrep-checker/) is a useful plugin that will embed it into the page.
3. Optionally enter a specific map to find demos for, or the SteamID64 of a user they may have played with.
3. Press `Go` and the results window will open.

You can get the demo from this by clicking on the link, pressing `Ctrl+C`, and entering it into your web browser.

## Building
Requires **[Python 3.11](https://www.python.org/downloads/)** or later.

1. Install `pyinstaller`
```
python -m pip install pyinstaller
```
2. Run `pyinstaller --onefile -n utdemofinder --clean --noconsole main.py`
