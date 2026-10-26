"""The middle mouse button goes to the definition under it in warp files (Default.sublime-mousemap). Mousemaps take no
context, so the warp test is here; elsewhere the click stays the default column select."""
import sublime_plugin


class WarpDefinitionClickCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        clicked_without_dragging = len(selection) == 1 and selection[0].empty()
        if clicked_without_dragging and self.view.match_selector(selection[0].a, "source.warp"):
            self.view.window().run_command("goto_definition")
