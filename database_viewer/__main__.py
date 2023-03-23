import dearpygui.dearpygui as dpg
import sqlite3
from sys import exit
import webbrowser

# Setup our context and viewport
dpg.create_context()
dpg.create_viewport(title='Database Viewer', width=800, height=600)

# Initalize global variables used to interact with the database
db_file = ""
connection = None
cur = None
current_table = ""

# Setup our fonts
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("fonts/opensans.ttf", 16)
    title_font = dpg.add_font("fonts/opensans.ttf", 48)
    header_font = dpg.add_font("fonts/opensans.ttf", 28)

def show_database(sender, app_data):
    """This function takes the database file and loads all the tables inside of it into tabs on the tab bar"""

    # We first clear all the children of the tab bar
    dpg.delete_item("tab_bar", children_only=True)

    # Next we get the tables from the db
    global db_file, connection, cur, current_table
    db_file = app_data["file_path_name"]
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # We update the label to show what file is selected
    dpg.configure_item("database_file", label=app_data["file_name"])

    # Loop through all the tables and add them as tabs
    tables = cur.fetchall()
    for table in tables:
        t = table[0]
        dpg.add_tab(parent="tab_bar", label=t, tag=t)

    # Set our current table
    current_table = tables[0][0]
    connection.close()

    # Finally populate the table with data
    populate_db(None, current_table)

def populate_db(sender, data):
    # Delete the table if there is one and add a new one
    dpg.delete_item("data")
    dpg.add_table(tag="data", parent=data)

    # Reconnect to the db and get all the headers
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()
    cur.execute("SELECT name FROM pragma_table_info(:table)", ({"table" : data}))

    # Add the headers to the table
    for header in cur.fetchall():
        dpg.add_table_column(parent="data", label=header[0])
    
    # Finally add the data from the db to the table
    cur.execute(f"SELECT * FROM {data}")
    for x in cur.fetchall():
        with dpg.table_row(parent="data"):
            for y in x:
                dpg.add_text(y)
    

def select_table(sender, data):
    """Changes what table is currently selected"""
    global current_table
    current_table = sender
    populate_db(None, sender)

with dpg.file_dialog(directory_selector=False, show=False, callback=show_database, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension("Databases (*.sqlite *.sqlite3 *.db){.sqlite,.sqlite3,.db}", color=(0, 255, 255, 255))

# About Window
with dpg.window(label="About", tag="About", show=False, width=400, height=490):
    b2 = dpg.add_text("SQLite Viewer 1.0.0")
    dpg.add_text("Made by grqphical07")
    dpg.add_spacer()
    b3 = dpg.add_text("Licensed under the MIT License:")
    dpg.add_input_text(default_value="""
Copyright (c) 2023 grqphical07

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""", multiline=True, readonly=True, width=390, height=390)

    dpg.bind_font(default_font)
    dpg.bind_item_font(b2, title_font)
    dpg.bind_item_font(b3, header_font)

with dpg.window(label="Example Window", tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Select File", callback=lambda: dpg.show_item("file_dialog_id"))
            dpg.add_menu_item(label="Exit", shortcut="Alt+F4", callback=lambda: exit())

        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About", callback=lambda: dpg.configure_item("About", show=True))
            dpg.add_menu_item(label="Github")
    
    b2 = dpg.add_text("SQLite Viewer")
    dpg.add_spacer()
    dpg.add_button(label="Select Database", callback=lambda: dpg.show_item("file_dialog_id"), tag="database_file")
    
    dpg.add_tab_bar(tag="tab_bar", callback=populate_db)
    dpg.bind_font(default_font)
    dpg.bind_item_font(b2, title_font)

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)


dpg.bind_theme(global_theme)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()