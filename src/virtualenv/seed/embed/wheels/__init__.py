from __future__ import absolute_import, unicode_literals
from subprocess import check_output, CalledProcessError

from virtualenv.util.path import Path

BUNDLE_SUPPORT = {
    "3.9": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-46.1.3-py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
    "3.8": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-46.1.3-py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
    "3.7": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-46.1.3-py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
    "3.6": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-46.1.3-py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
    "3.5": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-46.1.3-py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
    "3.4": {
        "pip": "pip-19.1.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-43.0.0-py2.py3-none-any.whl",
        "wheel": "wheel-0.33.6-py2.py3-none-any.whl",
    },
    "2.7": {
        "pip": "pip-20.1-py2.py3-none-any.whl",
        "setuptools": "setuptools-44.1.0-py2.py3-none-any.whl",
        "wheel": "wheel-0.34.2-py2.py3-none-any.whl",
    },
}
MAX = "3.9"


# The mapping above is overwritten by the code below this comment.
# It's intentionaly left here so the patch will stay the same even
# for future changes of the versions.
class SystemWheels:
    def __getitem__(self, creator):
        bundled = ["pip", "setuptools", "wheel"]
        # creator might be an instance of the internal Creator object
        # or str/Path with a path to Python executable
        if isinstance(creator, str):
            executable = creator
        else:
            executable = creator.exe
        paths = []
        result = {}

        # ensurepip path
        # We need subprocess here to check ensurepip with the Python we are creating
        # a new virtual environment for
        try:
            ensurepip_path = check_output((executable, "-u", "-c",
                                           'import ensurepip; print(ensurepip.__path__[0])'),
                                          universal_newlines=True)
            ensurepip_path = Path(ensurepip_path.strip()) / "_bundled"
        except CalledProcessError:
            pass
        else:
            if ensurepip_path.is_dir():
                paths.append(ensurepip_path)

        # Standard wheels path
        wheels_dir = Path("/usr/share/python-wheels")
        if wheels_dir.exists():
            paths.append(wheels_dir)

        # Find and use the first wheel for all bundled packages
        # ensurepip takes precedence (if exists)
        for package in bundled:
            result[package] = None
            for path in paths:
                wheels = list(path.glob(package + "-*.whl"))
                if wheels:
                    result[package] = wheels[0]
                    break

        return result

    def get(self, key, default=None):
        return self.__getitem__(key)


BUNDLE_SUPPORT = SystemWheels()

# We should never ever need this but it has to stay importable
MAX = None
