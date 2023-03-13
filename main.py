###
#   utdemofinder
#
#   Uncletopia website API helper app for finding demos
#
#   Jack Avery 2023
###
import json
import os
import requests
import re
import tkinter as tk
version = '1.0.2'

STEAMID_RE = re.compile(r"\d+")
"""Regex to compare Steam UserID64s to to validate"""

CONFIG_PATH = "config.txt"
"""Path to the user config file to use"""

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('480x280')
        self.root.title(f"utdemofinder {version}")
        self.root.configure(bg="#444444")
        self.root.resizable(0, 0)

        demo_folder = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf"
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as cfgfile:
                cfg = json.loads(cfgfile.read())
            demo_folder = cfg["demo_folder"]

        tk.Label(master=self.root, text="Demo folder:", bg="#444444", fg="white")\
            .place(x=0, y=0, width=70, height=24)
        self.folder_input = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8, wrap="none")
        self.folder_input.place(x=76, y=0, width=404, height=24)
        self.folder_input.insert(tk.END, demo_folder)

        tk.Label(master=self.root, text="Steam ID64:", bg="#444444", fg="white")\
            .place(x=0, y=24, width=64, height=24)
        self.search_id64 = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8, wrap="none")
        self.search_id64.place(x=70, y=24, width=410, height=24)

        tk.Label(master=self.root, text="Map:", bg="#444444", fg="white")\
            .place(x=0, y=48, width=64, height=24)
        self.search_map = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8, wrap="none")
        self.search_map.place(x=70, y=48, width=410, height=24)

        tk.Label(master=self.root, text="Played With:", bg="#444444", fg="white")\
            .place(x=0, y=72, width=64, height=24)
        self.search_with = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8, wrap="none")
        self.search_with.place(x=70, y=72, width=410, height=24)

        self.go = tk.Button(
            text="Go", command=self.get_demos, bg="#004400", fg="white")
        self.go.place(x=0, y=96, width=480, height=36)

        self.infobox = tk.Listbox(self.root, bg="#444444", fg="white")
        self.infobox.place(x=0, y=132, width=480, height=148)

        self.log("Enter a Steam ID64 and press Go.")
        self.log("A new window will open up with the results.")
        self.log("\"Map\" and \"Played With\" are optional.")
        tk.mainloop()

    def get_demos(self):
        """
        Get the demos with the options specified.
        """
        self.log("")
        self.log("Searching...")

        demofolder = self.folder_input.get("1.0", "end-1c")
        id = self.search_id64.get("1.0", "end-1c")
        map = self.search_map.get("1.0", "end-1c")
        id_with = self.search_with.get("1.0", "end-1c")

        with open(CONFIG_PATH, "w") as cfgfile:
            data = {
                "demo_folder": demofolder
            }

            cfgfile.writelines(json.dumps(data, indent=4))

        if not STEAMID_RE.match(id):
            self.log("Invalid ID64 for \"Steam ID\".")
            return

        if id_with:
            if not STEAMID_RE.match(id_with):
                self.log("Invalid ID64 for \"Played With\".")
                return

        data = {
            "steamId":id,
            "mapName":map,
            "serverIds":[] # todo: create reasonable UI for this?
        }

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*"
        }

        response = requests.post("https://uncletopia.com/api/demos", json=data, headers=headers)
        if response.status_code != 201:
            self.log(f"Returned {response.status_code}: cannot continue")
            return

        results = response.json()["result"]
        if not results:
            self.log(f"Couldn't find any demos for this user!")
            return

        self.log(f"Found {len(results)} demo(s)")

        if id_with:
            self.log(f"Sorting to demos with {id_with}...")
            sorted = []
            for result in results:
                if id_with in result['stats']:
                    sorted.append(result)
            results = sorted
            self.log(f"Cut down to {len(results)}")

        _ = ResultsWindow(results)

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)

class ResultsWindow:
    def __init__(self, resultslist: list):
        self.root = tk.Tk()
        self.root.geometry('480x280')
        self.root.title(f"utdemofinder {version}: results")
        self.root.configure(bg="#444444")

        self.infobox = tk.Listbox(self.root, bg="#444444", fg="white")
        self.infobox.pack(fill=tk.BOTH, expand=1)

        for i, result in enumerate(resultslist):
            self.infobox.insert(tk.END, f"Result #{i+1}:")
            self.infobox.insert(tk.END, f"https://uncletopia.com/demos/{result['demo_id']}")
            self.infobox.insert(tk.END, f"Server: {result['server_name_long']} ({result['server_name_short']})")
            self.infobox.insert(tk.END, f"Map: {result['map_name']}")
            self.infobox.insert(tk.END, f"Time: {result['created_on']}")
            self.infobox.insert(tk.END, "")

if __name__ == "__main__":
    _ = Application()