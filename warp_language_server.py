# warp's language server in Sublime's LSP package: go to definition (F12) and hover for .warp files, answered by
# scripts/lsp.warp of the warp repository (card language-server). Its command is in LSP-warp.sublime-settings
from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin


class Warp(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return "warp"


def plugin_loaded() -> None:
    register_plugin(Warp)


def plugin_unloaded() -> None:
    unregister_plugin(Warp)
