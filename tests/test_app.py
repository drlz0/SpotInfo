import pytest
import tkinter as tk
from src.application.main import Application


@pytest.fixture(scope="module")
def app():
    root = tk.Tk()
    app = Application(root)
    yield app
    root.destroy()


def test_text_default(app):
    assert app.text_label.cget("text") == "Input name"
    assert app.bt_ok.cget("text") == "OK"


# def test_text_box_exist(app):
#     assert isinstance(app.text_box, ScrolledText)

def test_text_box_initial_value(app):
    assert app.text_box.get("1.0", "end-1c") == ""


def test_text_box_insert_text(app):
    text = "test text"
    app.text_box.insert(tk.END, text)
    assert app.text_box.get("1.0", "end-1c") == text


def test_is_func_retrieve_working(app):
    text = "Slayer"
    app.text_box.insert(tk.END, text)
    assert app.retrieve_input() != "asdf"
