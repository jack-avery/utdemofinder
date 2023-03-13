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
from tkinter import filedialog
import urllib3
version = '1.2.0'

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

        tk.Button(self.root, text="Go", command=self.get_demos, bg="#004400", fg="white")\
            .place(x=0, y=96, width=480, height=36)

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

        _ = ResultsWindow(demofolder, id, results)

    def log(self, l: str):
        """
        Log information to the info box and force the view to the bottom.
        """
        self.infobox.insert(tk.END, f"{l}")
        self.infobox.yview(tk.END)

class ResultsWindow:
    def __init__(self, demofolder: str, uid: str, resultslist: list):
        self.root = tk.Tk()
        self.root.geometry('480x128')
        self.root.title(f"utdemofinder {version}: results")
        self.root.configure(bg="#444444")
        self.root.resizable(0, 0)

        self.demofolder = demofolder
        self.uid = uid
        self.resultslist = resultslist
        self.viewindex = 0

        tk.Button(self.root, text="Save all results to file", command=self.save_to_file, bg="#555555", fg="white")\
            .place(x=0, y=0, width=128, height=24)
        tk.Button(self.root, text="Download this results' demo", command=self.download_demo, bg="#555555", fg="white")\
            .place(x=130, y=0, width=164, height=24)

        tk.Button(self.root, text="<", command=self.display_last, bg="#444444", fg="white")\
            .place(x=0, y=24, width=24, height=104)
        tk.Button(self.root, text=">", command=self.display_next, bg="#444444", fg="white")\
            .place(x=456, y=24, width=24, height=104)
        
        self.result_text = tk.Text(self.root, bg="#444444", fg="white")
        self.result_text.place(x=24, y=24, width=438, height=104)

        self.display_result()
        tk.mainloop()
    
    def display_last(self):
        if self.viewindex == 0:
            return
        
        self.viewindex -= 1
        self.display_result(self.viewindex)
    
    def display_next(self):
        if self.viewindex == len(self.resultslist)-1:
            return
        
        self.viewindex += 1
        self.display_result(self.viewindex)

    def display_result(self, index: int = 0):
        self.result_text.delete("1.0", "end-1c")
        self.result_text.insert(tk.END, f"Result #{index+1} of {len(self.resultslist)}:\n")
        self.result_text.insert(tk.END, self.text_result(self.resultslist[index]))

    def download_demo(self, index: int = 0):
        result = self.resultslist[index]
        url = f"https://uncletopia.com/demos/{result['demo_id']}"
        path = f"{self.demofolder}/{result['title']}"

        http = urllib3.PoolManager()
        r = http.request('GET', url, preload_content=False)
        with open(path, 'wb') as out:
            while True:
                data = r.read(4096)
                if not data:
                    break
                out.write(data)
        r.release_conn()
    
    def text_result(self, result):
        text = ""
        text += f"https://uncletopia.com/demos/{result['demo_id']}\n"
        text += f"Server: {result['server_name_long']} ({result['server_name_short']})\n"
        text += f"Map: {result['map_name']}\n"
        text += f"Time: {result['created_on']}\n\n"
        return text

    def save_to_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[('Text files', '*.txt')],
            initialdir=os.curdir,
            initialfile=f"utdemofinder results - {self.uid}"
        )

        if not filename:
            return

        resultslist_raw = ""
        for result in self.resultslist:
            resultslist_raw += self.text_result(result)

        with open(filename, "w") as file:
            file.write(resultslist_raw)

if __name__ == "__main__":
    _ = Application()