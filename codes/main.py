
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.widgets import Frame

import functions
import personalized

def main():

    choices = [
        "Add new event",
        "Display specific event(s) in detail",
        "Delete Specific Event(s)",
        "Make new data chunk",
        "Display specific data chunk(s) in detail",
        "Delete Specific Chunk(s)",
        "Make file output",
        "Send Personalized Certs",
        "Exit"
    ]

    selected = 0
    result = None

    # --------------------------------------------------
    # MENU RENDERING
    # --------------------------------------------------

    def get_menu_column(column):

        def render():
            fragments = []

            for row in range(3):
                index = row + column * 3

                if index >= len(choices):
                    continue

                number = f"{index + 1:02}"
                name = choices[index]

                if index == selected:
                    fragments.append((
                        "class:selected",
                        f"  ❯ {number}  {name}\n"
                    ))
                else:
                    fragments.append((
                        "class:normal",
                        f"    {number}  {name}\n"
                    ))

            return fragments

        return FormattedTextControl(render)

    # --------------------------------------------------
    # MENU LAYOUT
    # --------------------------------------------------

    def get_layout():

        menu = VSplit([
            Window(
                get_menu_column(0),
                width=43,
                height=3,
            ),
            Window(
                get_menu_column(1),
                width=49,
                height=3,
            ),
            Window(
                get_menu_column(2),
                height=3,
            ),
        ])

        return Layout(
            HSplit([
                Frame(
                    menu,
                    title=" LETTO / MAIN MENU ",
                    style="class:frame"
                ),
                Window(
                    FormattedTextControl(
                        HTML(
                            "<ansibrightblack>"
                            "  ↑ ↓ Navigate  |  ← → Switch column  |  "
                            "Enter Select  |  Ctrl+C Exit"
                            "</ansibrightblack>"
                        )
                    ),
                    height=1
                )
            ])
        )

    # --------------------------------------------------
    # KEYBOARD CONTROLS
    # --------------------------------------------------

    kb = KeyBindings()

    @kb.add("up")
    def up(event):
        nonlocal selected
        selected = (selected - 1) % len(choices)

    @kb.add("down")
    def down(event):
        nonlocal selected
        selected = (selected + 1) % len(choices)

    @kb.add("left")
    def left(event):
        nonlocal selected
        selected = (selected - 3) % len(choices)

    @kb.add("right")
    def right(event):
        nonlocal selected
        selected = (selected + 3) % len(choices)

    @kb.add("enter")
    def enter(event):
        nonlocal result
        result = choices[selected]
        event.app.exit()

    @kb.add("c-c")
    def exit_menu(event):
        event.app.exit()

    # --------------------------------------------------
    # MENU STYLE
    # --------------------------------------------------

    style = Style.from_dict({
        "frame": "fg:#00d7ff",
        "selected": "fg:#00d7ff bold",
        "normal": "fg:#c0c0c0",
    })

    # --------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------

    while True:

        result = None

        app = Application(
            layout=get_layout(),
            key_bindings=kb,
            style=style,
            full_screen=False,
            mouse_support=True
        )

        print("\n")
        app.run()

        if result is None:
            break

        # --------------------------------------------------
        # EXECUTE SELECTED FUNCTION
        # --------------------------------------------------

        if result == "Add new event":
            functions.add_new_event()

        elif result == "Display specific event(s) in detail":
            functions.display_events_detail()

        elif result == "Delete Specific Event(s)":
            functions.delete_events()

        elif result == "Make new data chunk":
            functions.create_chunk()

        elif result == "Display specific data chunk(s) in detail":
            functions.show_chunks()

        elif result == "Delete Specific Chunk(s)":
            functions.delete_chunks()

        elif result == "Make file output":
            functions.file_output()

        elif result == "Send Personalized Certs":
            personalized.personalized_mails()

        elif result == "Exit":
            print("")
            break

if __name__ == "__main__":
    main()