import json
import os
import re
import tkinter as tk
from tkinter import filedialog

import requests

from src.results import ResultsWindow
from src.defines import *

STEAMID_RE = re.compile(r"\d+")
"""Regex to compare Steam UserID64s to to validate"""


class SearchWindow:
    """
    `tkinter`-based GUI for finding user demos from Uncletopia based on some basic user-defined criteria.
    """

    def __init__(self):
        """
        Create a new instance of a `utdemofinder` GUI window.
        """
        self.root = tk.Tk()
        self.root.geometry("480x280")
        self.root.title(f"utdemofinder {VERSION} search")
        self.root.configure(bg="#444444")
        self.root.resizable(0, 0)

        # Demo folder: [...] [Folder Display]
        tk.Label(master=self.root, text="Demo folder:", bg="#444444", fg="white").place(
            x=0, y=0, width=70, height=24
        )
        tk.Button(
            self.root, text="...", command=self.get_folder, bg="#555555", fg="white"
        ).place(x=76, y=0, width=24, height=24)
        self.folder_input = tk.Text(
            master=self.root, bg="#440000", fg="white", height=1, width=8, wrap="none"
        )
        self.folder_input.place(x=100, y=0, width=380, height=24)

        demo_folder = PROMPT_FOLDER_TEXT
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as cfgfile:
                cfg = json.loads(cfgfile.read())
            demo_folder = cfg["demo_folder"]
        self.set_folder_input(demo_folder)

        # Steam ID64: [Text Input]
        tk.Label(master=self.root, text="Steam ID64:", bg="#444444", fg="white").place(
            x=0, y=24, width=64, height=24
        )
        self.search_id64 = tk.Text(
            master=self.root, bg="#333333", fg="white", height=1, width=8, wrap="none"
        )
        self.search_id64.place(x=70, y=24, width=410, height=24)

        # Map: [Text Input]
        tk.Label(master=self.root, text="Map:", bg="#444444", fg="white").place(
            x=0, y=48, width=64, height=24
        )
        self.search_map = tk.Text(
            master=self.root, bg="#333333", fg="white", height=1, width=8, wrap="none"
        )
        self.search_map.place(x=70, y=48, width=410, height=24)

        # Played With: [Text Input]
        tk.Label(master=self.root, text="Played With:", bg="#444444", fg="white").place(
            x=0, y=72, width=64, height=24
        )
        self.search_with = tk.Text(
            master=self.root, bg="#333333", fg="white", height=1, width=8, wrap="none"
        )
        self.search_with.place(x=70, y=72, width=410, height=24)

        # [Go]
        tk.Button(
            self.root, text="Go", command=self.get_demos, bg="#004400", fg="white"
        ).place(x=0, y=96, width=480, height=36)

        # Activity Log
        self.infobox = tk.Listbox(self.root, bg="#333333", fg="white")
        self.infobox.place(x=0, y=132, width=480, height=148)

        self.log("Enter a Steam ID64 and press Go.")
        self.log("A new window will open up with the results.")
        self.log('"Map" and "Played With" are optional.')
        tk.mainloop()

    def get_folder(self):
        """
        Prompts the user for a folder to save demo files to.
        """
        folder = filedialog.askdirectory(initialdir="/")
        if not folder:
            return

        self.set_folder_input(folder)
        with open(CONFIG_PATH, "w") as cfgfile:
            data = {"demo_folder": folder}

            cfgfile.writelines(json.dumps(data, indent=4))

    def set_folder_input(self, folder):
        """
        Set the value of `tkinter.Text` widget `Application.folder_input` and update the color to green if it's a user-defined folder.

        :param folder: The user-defined path or prompt for user selection.
        """
        self.folder_input.configure(state=tk.NORMAL)
        self.folder_input.delete("1.0", "end-1c")
        self.folder_input.insert(tk.END, folder)
        self.folder_input.configure(state=tk.DISABLED)

        if folder != PROMPT_FOLDER_TEXT:
            self.folder_input.configure(bg="#004400")

    def get_demos(self):
        """
        Get user demos from the specified criteria and open the results window.
        """
        self.log("")
        self.log("Searching...")

        demofolder = self.folder_input.get("1.0", "end-1c")
        id = self.search_id64.get("1.0", "end-1c")
        map = self.search_map.get("1.0", "end-1c")
        id_with = self.search_with.get("1.0", "end-1c")

        if not STEAMID_RE.match(id):
            self.log('Invalid ID64 for "Steam ID".')
            return

        if id_with:
            if not STEAMID_RE.match(id_with):
                self.log('Invalid ID64 for "Played With".')
                return

        data = {
            "steamId": id,
            "mapName": map,
            "serverIds": [],  # todo: create reasonable UI for this?
        }

        headers = {"Content-Type": "application/json; charset=UTF-8", "Accept": "*/*"}

        response = requests.post(
            "https://uncletopia.com/api/demos", json=data, headers=headers
        )
        if response.status_code != 201:
            self.log(f"Returned {response.status_code}: cannot continue")
            return
        results = response.json()["result"]

        if id_with and results:
            sorted = []
            for result in results:
                if id_with in result["stats"]:
                    sorted.append(result)
            results = sorted

        if not results:
            self.log(f"Couldn't find any demos with this criteria!")
            return

        self.log(f"Found {len(results)} demo(s)")
        _ = ResultsWindow(demofolder, id, results)

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.

        :param l: The text to log.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)

if __name__ == "__main__":
    _ = SearchWindow()