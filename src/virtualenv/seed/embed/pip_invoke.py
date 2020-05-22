from __future__ import absolute_import, unicode_literals

import logging
from contextlib import contextmanager

from virtualenv.discovery.cached_py_info import LogCmd
from virtualenv.info import PY3
from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.embed.wheels.acquire import get_bundled_wheel, pip_wheel_env_run
from virtualenv.util.subprocess import Popen
from virtualenv.util.zipapp import ensure_file_on_disk

if PY3:
    from contextlib import ExitStack
else:
    from contextlib2 import ExitStack


class PipInvoke(BaseEmbed):
    def __init__(self, options):
        super(PipInvoke, self).__init__(options)

    def run(self, creator):
        if not self.enabled:
            return
        self.insert_system_wheels_paths(creator)
        with self.get_pip_install_cmd(creator.exe, creator.interpreter.version_release_str) as cmd:
            with pip_wheel_env_run(creator.interpreter.version_release_str, creator.interpreter.executable, self.app_data) as env:
                self._execute(cmd, env)

    @staticmethod
    def _execute(cmd, env):
        logging.debug("pip seed by running: %s", LogCmd(cmd, env))
        process = Popen(cmd, env=env)
        process.communicate()
        if process.returncode != 0:
            raise RuntimeError("failed seed with code {}".format(process.returncode))
        return process

    @contextmanager
    def get_pip_install_cmd(self, exe, version):
        cmd = [str(exe), "-m", "pip", "-q", "install", "--only-binary", ":all:"]
        if not self.download:
            cmd.append("--no-index")
        pkg_versions = self.package_version()
        for key, ver in pkg_versions.items():
            cmd.append("{}{}".format(key, "=={}".format(ver) if ver is not None else ""))
        with ExitStack() as stack:
            folders = set()
            folders.update(set(self.extra_search_dir))
            for folder in folders:
                cmd.extend(["--find-links", str(folder)])
            yield cmd
