from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Label, ListItem, ListView

CONTENT_MAP = {
    "overview": "Welcome to the Dashboard!\n\nThis is the main panel. Use the command line below to interact.",
    "settings": "Settings Configuration:\n\n[ ] Enable notifications\n[x] Dark mode active",
    "profile": "User Profile:\n\nUsername: TUI_Developer\nRole: Administrator",
    "logs": "System Logs:\n\n12:00:00 - App started successfully.\n12:01:45 - Command processor initialized.",
}

class SidebarApp(App):
    CSS = """
    Horizontal {
        height: 1fr;
    }
    
    #sidebar {
        width: 30;
        background: $surface;
        border-right: solid $background;
    }
    
    #main-panel {
        padding: 1;
        background: $panel;
    }
    
    #content-text {
        margin-top: 1;
    }
    
    Input {
        dock: bottom;
        border: none;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("  Navigation", id="sidebar-title")
                yield ListView(
                    *[ListItem(Label(item.capitalize()), id=item) for item in CONTENT_MAP.keys()],
                    id="sidebar-list"
                )
            with Vertical(id="main-panel"):
                yield Label("Content View", variant="title")
                yield Label(CONTENT_MAP["overview"], id="content-text")
        
        yield Input(placeholder=":command", value=":")
        yield Footer()

    def on_list_view_selected(self, message: ListView.Selected) -> None:
        item_id = message.item.id
        content_label = self.query_one("#content-text", Label)
        content_label.update(CONTENT_MAP.get(item_id, "No content found."))

    def on_input_submitted(self, message: Input.Submitted) -> None:
        cmd = message.value.strip()
        
        if cmd in (":q", ":quit"):
            self.exit()
        elif cmd.startswith(":view "):
            parts = cmd.split(" ", 1)
            if len(parts) > 1:
                target = parts[1].strip().lower() 
                
                if target in CONTENT_MAP:
                    content_label = self.query_one("#content-text", Label)
                    content_label.update(CONTENT_MAP[target])
                    
                    sidebar_list = self.query_one("#sidebar-list", ListView)
                    for index, item in enumerate(sidebar_list.children):
                        if item.id == target:
                            sidebar_list.index = index
                            break
        
        message.input.value = ":"

    def on_input_changed(self, message: Input.Changed) -> None:
        if not message.value.startswith(":"):
            message.input.value = ":"

if __name__ == "__main__":
    app = SidebarApp()
    app.run()
