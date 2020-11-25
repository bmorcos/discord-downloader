import os
import configparser


cfg_defaults = {
    "args": {
        "after": None,
        "before": None,
        "channels": None,
        "dry_run": False,
        "exclude_str": None,
        "filetypes": None,
        "include_str": None,
        "num_messages": 200,
        "output_dir": os.getcwd(),
        "prepend_user": False,
        "server": None,
        "verbose": False,
        "zipped": False,
    },
}


install_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# The cfg files in the order in which they will be read (and given precedence)
cfg_files = [
    os.path.join(install_dir, "config"),
]


class _CFG(configparser.ConfigParser):
    def __init__(self):
        # configparser uses old-style classes without 'super' support
        configparser.ConfigParser.__init__(self, allow_no_value=True)
        self.reload_cfg()

    def _clear(self):
        self.remove_section(configparser.DEFAULTSECT)
        for s in self.sections():
            self.remove_section(s)

    def _init_defaults(self):
        for section, settings in cfg_defaults.items():
            self.add_section(section)
            for k, v in settings.items():
                if v is None:
                    self.set(section, k)
                else:
                    self.set(section, k, str(v))

    def read(self, filenames):
        return configparser.ConfigParser.read(self, filenames)

    def reload_cfg(self, filenames=None):
        """Resets the currently loaded RC settings and loads new RC files.

        Parameters
        ----------
        filenames: iterable object
            Filenames of RC files to load.
        """
        defaults = False
        if filenames is None:
            filenames = cfg_files
            defaults = True  # There may be no cfg files when using defaults

        self._clear()
        self._init_defaults()
        read_ok = self.read(filenames)

        if not defaults and len(read_ok) < 1:
            raise RuntimeError(
                "Unable to read specified config file(s): {}".format(filenames)
            )


cfg = _CFG()
