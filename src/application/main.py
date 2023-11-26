import tkinter as tk
from tkinter import ttk
import requests
import pandas as pd
import base64
import secrets
import os
from dotenv import load_dotenv


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.table_data_x = None
        self.n_status = None

        load_dotenv()

        self.master = master
        self.ENDPOINT = "https://api.spotify.com/v1"
        self.redirect_uri = 'http://localhost:8888/callback'
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')

        self.text_label = tk.Label(self, text="Input name")
        self.text_label.grid(row=0, column=0, padx=5, pady=30)

        self.text_box = tk.Text(self, height=1, width=20)
        self.text_box.grid(row=0, column=1, padx=5, pady=30)

        self.bt_ok = tk.Button(self, text="OK", command=self.authorize_and_fetch_data)
        self.bt_ok.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        self.result_label = tk.Label(self)
        self.result_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.pack()

    @staticmethod
    def generate_random_string(length):
        return secrets.token_urlsafe(length)

    def authorize_spotify(self):
        state = self.generate_random_string(16)
        scope = 'user-read-private'

        authorize_url = f'https://accounts.spotify.com/authorize?client_id={self.client_id}&' \
                        f'response_type=code&scope={scope}&redirect_uri={self.redirect_uri}&state={state}'

        print(f"Please go to this URL to authorize your application: {authorize_url}")

        # Manually open this URL in your browser and get the authorization code
        auth_code = input("Enter the authorization code: ")

        return auth_code

    def retrieve_input(self, auth_code):
        # variable to cancel table creating
        self.n_status = True
        # get name from text box
        name = self.text_box.get("1.0", 'end-1c')

        # Exchange authorization code for access token
        token_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f'{self.client_id}:'
                                                         f'{self.client_secret}'.encode('utf-8')).decode('utf-8')
        }
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(token_url, headers=headers, data=payload)
        token_info = response.json()

        if 'access_token' not in token_info:
            self.result_label.config(text="Error getting access token")
            self.n_status = False
            return self.n_status

        access_token = token_info['access_token']

        # get artist id
        url_for_id = f"https://api.spotify.com/v1/search?q={name}&type=artist"
        headers = {'Authorization': f'Bearer {access_token}'}

        get_id = requests.get(url_for_id, headers=headers)
        get_id_json = get_id.json()

        if get_id_json["artists"]["total"] != 0:
            artist_id = get_id_json["artists"]["items"][0]["id"]
        else:
            self.result_label.config(text="Invalid Name")
            self.n_status = False
            return self.n_status

        # get artist albums from id
        url_for_albums = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50&include_groups=album"
        get_albums = requests.get(url_for_albums, headers=headers)
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

    def authorize_and_fetch_data(self):
        auth_code = self.authorize_spotify()
        if not auth_code:
            return
        self.retrieve_input(auth_code)
        if not self.n_status:
            return
        self.create_table()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SpotInfo")
    root.geometry("450x200")
    app = Application(master=root)
    app.mainloop()
