## utdemofinder

**utdemofinder** is a utility program for the video game servers **Uncletopia** for **Team Fortress 2** to provide a simple user interface for moderators to search for SourceTV demos for specific users, including games played with other users.

![utdemofinder](https://cdn.discordapp.com/attachments/488850419301220352/1084981187388375100/image.png)

## Usage
1. Download and install [Python version 3.11.0+](https://www.python.org/downloads/), ensuring you tick "Add python.exe to PATH" at the bottom of the first screen.
2. Download the Source Code:
> Using [git](https://git-scm.com/downloads): `git clone https://github.com/jack-avery/utdemofinder` <br/>
> Or, click on **Code** at the top right and **Download ZIP**.
3. Install dependencies: `python -m pip install -r requirements.txt`.
4. Open `main.py`.
5. Insert a valid ID into the Steam ID64 field.
> This normally looks something like `76561198027298961`<br/>
6. Press `Go` and the results window will open.

I recommend you enter your `steamapps/common/Team Fortress 2/tf` folder into the "Demo folder" field so that you can download demos directly into your TF2 folder for easy access through `demoui`.
