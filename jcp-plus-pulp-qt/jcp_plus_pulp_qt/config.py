from typing import List, Any

from jcp_plus_pulp_core.config import load_config_toml


default_config = """
[jcp-plus-pulp-qt]
autostart_modules = ["jcp-plus-pulp-server", "jcp-plus-pulp-monitor-away", "jcp-plus-pulp-monitor-input", "jcp-plus-pulp-monitor-window", "jcp-plus-pulp-sync"]

[jcp-plus-pulp-qt-testing]
autostart_modules = ["jcp-plus-pulp-server", "jcp-plus-pulp-monitor-away", "jcp-plus-pulp-monitor-input", "jcp-plus-pulp-monitor-window", "jcp-plus-pulp-sync"]
""".strip()

class AwQtSettings:
    def __init__(self, testing: bool):
        """
        An instance of loaded settings, containing a list of modules to autostart.
        Constructor takes a `testing` boolean as an argument
        """
        config = load_config_toml("jcp-plus-pulp-qt", default_config)
        config_section: Any = config["jcp-plus-pulp-qt" if not testing else "jcp-plus-pulp-qt-testing"]

        self.autostart_modules: List[str] = config_section["autostart_modules"]
