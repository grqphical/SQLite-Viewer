import dearpygui.dearpygui as dpg
import sqlite3

dpg.create_context()
dpg.create_viewport(title='Database Viewer', width=800, height=600)

db_file = ""
connection = None
cur = None

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("fonts/jetbrains.ttf", 16)
    title_font = dpg.add_font("fonts/jetbrains.ttf", 36)

def show_database(sender, app_data):
    dpg.delete_item("data", children_only=True)

    global db_file, connection, cur
    db_file = app_data["file_path_name"]
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = []
    for table in cur.fetchall():
        tables.append(table[0])

    connection.close()

    dpg.configure_item("database_file", label=app_data["file_name"])
    dpg.configure_item("table_select", items=tables)

def populate_db():
    dpg.delete_item("data", children_only=True)

    table = dpg.get_value("table_select")
    connection = sqlite3.connect(db_file)
    cur = connection.cursor()
    cur.execute("SELECT name FROM pragma_table_info(:table)", ({"table" : table}))

    for header in cur.fetchall():
        dpg.add_table_column(parent="data", label=header[0])
    
    cur.execute(f"SELECT * FROM {table}")

    for x in cur.fetchall():
        with dpg.table_row(parent="data"):
            for y in x:
                dpg.add_text(y)
    
    

def cancel_callback(sender, app_data):
    print("Canceled")

with dpg.file_dialog(directory_selector=False, show=False, callback=show_database, id="file_dialog_id", width=700 ,height=400):
    dpg.add_file_extension("Databases (*.sqlite *.sqlite3 *.db){.sqlite,.sqlite3,.db}", color=(0, 255, 255, 255))

with dpg.window(label="Example Window", tag="Primary Window"):
    b2 = dpg.add_text("SQLite Viewer")
    dpg.add_spacer()
    dpg.add_button(label="Select Database", callback=lambda: dpg.show_item("file_dialog_id"), tag="database_file")
    dpg.add_combo(label="Table", tag="table_select", callback=populate_db)
    dpg.add_spacer()
    dpg.add_table(tag="data", row_background=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True)

    dpg.bind_font(default_font)
    dpg.bind_item_font(b2, title_font)

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)


dpg.bind_theme(global_theme)


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.show_style_editor()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()