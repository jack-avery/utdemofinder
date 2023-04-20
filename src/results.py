import logging
import os
import tkinter as tk
from tkinter import filedialog

import urllib3

from src.defines import *

logger = logging.getLogger("utdemofinder")


class ResultsWindow:
    """
    `tkinter`-based GUI for displaying user demos obtained using `src.search.SearchWindow`.
    """

    demofolder: str
    """The folder to save demos obtained through the 'Download demo' button to."""

    uid: str
    """The Steam ID64 that the demos in this result set belongs to."""

    resultslist: list
    """An array of dictionaries representing each demo found from `uncletopia.com/api/demos` and related metadata."""

    def __init__(self, demofolder: str, params: dict, resultslist: list):
        """
        Create a new instance of a `utdemofinder` results GUI window.

        :param demofolder: The folder to save demos obtained through the 'Download demo' button to.

        :param uid: `dict` containing the parameters used during search.

        :param resultslist: An array of dictionaries representing each demo found from `uncletopia.com/api/demos` and related metadata.
        """
        logger.info("Creating new Results Window")

        logger.debug(f"demofolder: {demofolder}")
        logger.debug(f"params: {params}")
        logger.debug(f"resultslist: ({len(resultslist)}) {resultslist}")

        self.root = tk.Tk()
        self.root.geometry("480x128")
        self.root.title(f"utdemofinder {VERSION} results: {params['id']}")
        self.root.configure(bg="#444444")
        self.root.resizable(0, 0)

        self.demofolder = demofolder
        self.params = params
        self.resultslist = resultslist
        self.viewindex = 0

        # User Tools
        tk.Button(
            self.root,
            text="Save all to file",
            command=self.save_to_file,
            bg="#555555",
            fg="white",
        ).place(x=0, y=0, width=86, height=24)
        if demofolder:
            tk.Button(
                self.root,
                text="Download demo",
                command=self.download_demo,
                bg="#555555",
                fg="white",
            ).place(x=88, y=0, width=102, height=24)

        # Navigation buttons
        tk.Button(
            self.root, text="<", command=self.display_last, bg="#444444", fg="white"
        ).place(x=0, y=24, width=24, height=104)
        tk.Button(
            self.root, text=">", command=self.display_next, bg="#444444", fg="white"
        ).place(x=456, y=24, width=24, height=104)

        # Result Info Box
        self.result_text = tk.Text(self.root, bg="#333333", fg="white")
        self.result_text.place(x=24, y=24, width=438, height=104)

        self.display_result()
        tk.mainloop()

    def display_last(self):
        """
        Display the previous result if applicable.
        """
        if self.viewindex == 0:
            self.viewindex = len(self.resultslist)

        self.viewindex -= 1
        self.display_result(self.viewindex)

    def display_next(self):
        """
        Display the next result if applicable.
        """
        if self.viewindex == len(self.resultslist) - 1:
            self.viewindex = -1

        self.viewindex += 1
        self.display_result(self.viewindex)

    def display_result(self, index: int = 0):
        """
        Clear the result text widget and insert information about the result at index `index` of `resultslist`.

        :param index: The index in `resultslist` to display.
        """
        logger.debug(
            f"showing result {index+1} of {len(self.resultslist)} ({self.resultslist[index]['demo_id']})"
        )

        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete("1.0", "end-1c")
        self.result_text.insert(
            tk.END, f"Result #{index+1} of {len(self.resultslist)}:\n"
        )
        self.result_text.insert(tk.END, self.text_result(self.resultslist[index]))
        self.result_text.configure(state=tk.DISABLED)

    def download_demo(self):
        """
        Download the currently viewed result to a user-defined folder.
        """
        result = self.resultslist[self.viewindex]
        url = f"https://uncletopia.com/demos/{result['demo_id']}"
        path = f"{self.demofolder}/{result['title']}"

        logger.info(f"Downloading demo #{result['demo_id']} to {path}...")

        http = urllib3.PoolManager()
        r = http.request("GET", url, preload_content=False)
        with open(path, "wb") as out:
            while True:
                data = r.read(4096)
                if not data:
                    break
                out.write(data)
        r.release_conn()

        logger.info(f"Download of demo #{result['demo_id']} completed")

    def text_result(self, result):
        """
        Convert `result` into a string for printing to the window or saving to disk.

        :param result: The result object as given from `uncletopia.com/api/demos`.
        """
        text = f"https://uncletopia.com/demos/{result['demo_id']}\n"
        text += (
            f"Server: {result['server_name_long']} ({result['server_name_short']})\n"
        )
        text += f"Map: {result['map_name']}\n"
        text += f"Time: {result['created_on']}\n\n"
        return text

    def save_to_file(self):
        """
        Save this `ResultsWindow`s' `resultslist` to a user-defined location on disk.
        """
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialdir=os.curdir,
            initialfile=f"utdemofinder results - {self.params['id']}",
        )

        if not filename:
            return

        resultslist_raw = ""
        resultslist_raw += f"Search results for {self.params['id']}"
        if self.params["id_with"]:
            resultslist_raw += f" played with {self.params['id_with']}"
        if self.params["map"]:
            resultslist_raw += f" on {self.params['map']}"
        resultslist_raw += "\n\n"

        for result in self.resultslist:
            resultslist_raw += self.text_result(result)

        logger.info(f"Saving results list to {filename}")

        with open(filename, "w") as file:
            file.write(resultslist_raw)
