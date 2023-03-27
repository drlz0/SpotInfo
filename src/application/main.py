import tkinter as tk
import requests
import pandas as pd
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.table_data_x = None
        self.n_status = None

        self.master = master
        self.ENDPOINT = "https://api.spotify.com/v1"
        self.auth = {
            'Authorization': "Bearer BQA-g0DqbR-FJsRuf2dQuyRkJs6EoKKbdKhQb1LmyT"
                             "BfOHDraRTo1E20z8a3AYX1B3TPHQl6QWOYCx-3HiZVe7Mz9wMk"
                             "vXGFoItxuq-1bZvNi090tHOJrzxpJUtgyMrTHEQdbo-CtDRinzU"
                             "a34jSftNH7fx7oVIFoAn03xOpzZQAS0ZIAm4uQNF5VDcs99D3Ev6"
                             "QgDPkJzuQgNcxHQH-5MMSzNWmWEHmCH15lukHpHiqY6o67Rsq5RoD3ec"
        }

        self.text_label = tk.Label(self, text="Input name")
        self.text_label.grid(row=0, column=0, padx=5, pady=30)

        self.text_box = tk.Text(self, height=1, width=20)
        self.text_box.grid(row=0, column=1, padx=5, pady=30)

        self.bt_ok = tk.Button(self, text="OK", command=self.combine)
        self.bt_ok.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        self.result_label = tk.Label(self)
        self.result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # self.buttonD = tk.Button(self.master, text="Open Table", command=self.create_table)
        # self.buttonD.pack()

        self.pack()

    def retrieve_input(self):
        # variable to cancel table creating
        self.n_status = True
        # get name from text box
        name = self.text_box.get("1.0", 'end-1c')
        url_for_id = f"https://api.spotify.com/v1/search?q={name}&type=artist"

        # get artist id
        get_id = requests.get(url_for_id, headers=self.auth)
        get_id_json = get_id.json()

        if get_id_json["artists"]["total"] != 0:
            artist_id = get_id_json["artists"]["items"][0]["id"]
        else:
            self.result_label.config(text="Invalid Name")
            self.n_status = False
            return self.n_status

        # get artist albums from id
        url_for_albums = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50&include_groups=album"

        get_albums = requests.get(url_for_albums, headers=self.auth)
        get_albums_json = get_albums.json()

        table_data_a = []

        self.table_data_x = []

        for x in get_albums_json["items"]:
            table_data_a.append(x["name"])
            table_data_a.append(x["release_date"])
            table_data_a.append(x["total_tracks"])

            self.table_data_x.append(table_data_a)

            table_data_a = []

        return self.table_data_x

    def create_dataframe(self):
        df = pd.DataFrame(self.table_data_x, columns=['Name of album', 'Release date', 'Total Tracks'])
        return df

    def create_table(self):
        table_window = tk.Toplevel(self.master)
        table_window.title("Table")
        table_window.geometry("1800x800")

        table = ttk.Treeview(table_window)
        table.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=table.yview)
        scrollbar.pack(side="right", fill="y")

        table.configure(yscrollcommand=scrollbar.set)

        df = self.create_dataframe()

        table["columns"] = list(df.columns)
        table["show"] = "headings"

        for column in table["columns"]:
            table.heading(column, text=column)

        for index, row in df.iterrows():
            table.insert("", "end", values=list(row))

    def combine(self):
        self.retrieve_input()
        if not self.n_status:
            return
        self.create_table()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SpotInfo")
    root.geometry("450x200")
    app = Application(master=root)
    app.mainloop()
