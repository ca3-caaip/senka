import os
import sys
import unittest

from senka.plugin_manager import PluginManager

sys.path.append("%s/plugin" % os.path.dirname(__file__))


class TestPluginManager(unittest.TestCase):
    def test_get_plugins(self):
        plugins = PluginManager.get_plugins(
            "test_one", "%s/test_senka_plugin.toml" % os.path.dirname(__file__)
        )
        assert len(plugins) == 1
        assert plugins[0].platform == "test_one"

    def test_get_plugins_exception(self):
        with self.assertRaises(RuntimeError):
            PluginManager.get_plugins(
                "test_none",
                "%s/test_senka_plugin_invalid.toml" % os.path.dirname(__file__),
            )


if __name__ == "__main__":
    unittest.main()
