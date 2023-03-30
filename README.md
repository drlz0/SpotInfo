# SpotInfo
Get band's or artist's albums

I was testing if github testing and tox testing works for TkInter, unfortunetly it can't.
Reason is that Tkinter uses Tcl/Tk, from Tkinter docs:

"The tkinter package is a thin object-oriented layer on top of Tcl/Tk.
To use tkinter, you don’t need to write Tcl code, but you will need to
consult the Tk documentation, and occasionally the Tcl documentation. 
tkinter is a set of wrappers that implement the Tk widgets as Python classes."

Tcl/Tk are another languages, so Tkinter is more like "software" than library, thus its impossile (or really complicated) for use Tkinter in tox and github testing
