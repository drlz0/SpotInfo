### SpotInfo
Get your band's albums info.
## GUI
![Screenshot_1](https://github.com/drlz0/SpotInfo/assets/121700730/813a4d58-44a2-4cf8-9ed8-b0cbc098714a)
![Screenshot_2](https://github.com/drlz0/SpotInfo/assets/121700730/e5efd8ca-1b36-4df5-84e2-a7a914d83f95)
## How to
1. Create .env file in root directory
2. Add your client_id and client_secret values to .env file from your Spotify API App page (https://developer.spotify.com/dashboard if you don't have app; create one)<br>
   content of .env should look like this:<br>
   CLIENT_ID=<your_client_id><br>
   CLIENT_SECRET=<your_client_secret><br>
3. Run main.py
4. Input band's name
5. Go to URL printed in console
6. Login with your creditials
7. You will be redirected to new page. It will probably display "page can not be reached", but thats fine. The important is the URL of that page. It's stuctured like this:<br>
   _http://localhost:8888/callback?code=**<your_authorization_code>**&state==<some_string>_<br>
   copy the code that begins from = and ends at & then input it into console after "Enter the authorization code: " that will be printed in new line after authorization URL<br>
8. Albums are listed in a table
   
# Tkinter with tox testing and github testing

I was testing if github testing and tox testing works for TkInter, unfortunetly it can't.
Reason is that Tkinter uses Tcl/Tk, from Tkinter docs:

"The tkinter package is a thin object-oriented layer on top of Tcl/Tk.
To use tkinter, you don’t need to write Tcl code, but you will need to
consult the Tk documentation, and occasionally the Tcl documentation. 
tkinter is a set of wrappers that implement the Tk widgets as Python classes."

Tcl/Tk are another languages, so Tkinter is more like "software" than library, thus its impossile (or really complicated) for use Tkinter in tox and github testing
