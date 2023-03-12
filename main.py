###
#   utdemofinder
#
#   Uncletopia website API helper app for finding demos
#
#   Jack Avery 2023
###
import requests
import re
import tkinter as tk
version = '1.0.1'

STEAMID_RE = re.compile(r"\d+")
"""Regex to compare Steam UserID64s to to validate"""

class Application:
    def __init__(self):
        # create the window
        self.root = tk.Tk()
        self.root.geometry('480x280')
        self.root.title(f"utdemofinder {version}")
        self.root.configure(bg="#444444")
        self.root.resizable(0, 0)

        # build UI
        # id64
        tk.Label(master=self.root, text="Steam ID64:", bg="#444444", fg="white")\
            .place(x=0, y=0, width=64, height=24)
        self.search_id64 = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8)
        self.search_id64.place(x=70, y=0, width=410, height=24)

        # map
        tk.Label(master=self.root, text="Map:", bg="#444444", fg="white")\
            .place(x=0, y=24, width=64, height=24)
        self.search_map = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8)
        self.search_map.place(x=70, y=24, width=410, height=24)

        tk.Label(master=self.root, text="Played With:", bg="#444444", fg="white")\
            .place(x=0, y=48, width=64, height=24)
        self.search_with = tk.Text(
            master=self.root, bg="#444444", fg="white", height=1, width=8)
        self.search_with.place(x=70, y=48, width=410, height=24)

        # logging info box for user notification
        self.infobox = tk.Listbox(self.root, bg="#444444", fg="white")
        self.infobox.place(x=0, y=108, width=480, height=172)

        # build the start and restore buttons but do not embed them for now.
        self.go = tk.Button(
            text="Go", command=self.get_demos, bg="#004400", fg="white")
        self.go.place(x=0, y=72, width=480, height=36)

        # open window and inform user to select a directory
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

        id = self.search_id64.get("1.0", "end-1c")
        map = self.search_map.get("1.0", "end-1c")
        id_with = self.search_with.get("1.0", "end-1c")

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
            "Accept": "*/*",
            "Host": "uncletopia.com",
            "Origin": "https://uncletopia.com",
            "Referer": "https://uncletopia.com/stv",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

        response = requests.post("https://uncletopia.com/api/demos", json=data, headers=headers)
        if response.status_code != 201:
            self.log(f"Returned {response.status_code}: cannot continue")

        result = response.json()["result"]

        if not result:
            self.log(f"Couldn't find any demos for this user!")
            return

        self.log(f"Found {len(result)} demo(s)")

        if id_with:
            self.log(f"Sorting to demos with {id_with}...")
            sorted = []
            for result in result:
                if id_with in result['stats']:
                    sorted.append(result)
            result = sorted
            self.log(f"Cut down to {len(result)}")

        _ = ResultsWindow(result)

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)

class ResultsWindow:
    def __init__(self, resultslist: list):
        # create the window
        self.root = tk.Tk()
        self.root.geometry('480x280')
        self.root.title(f"utdemofinder {version}: results")
        self.root.configure(bg="#444444")

        # create results box and populate
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
    app = Application()