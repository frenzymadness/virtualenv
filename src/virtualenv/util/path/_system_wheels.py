from subprocess import check_output, CalledProcessError

from virtualenv.util.path import Path


def get_system_wheels_paths(executable):
    # ensurepip wheels
    # We need subprocess here to check ensurepip with the Python we are creating
    # a new virtual environment for
    try:
        ensurepip_path = check_output((executable, "-u", "-c", 'import ensurepip; print(ensurepip.__path__[0])'), universal_newlines=True)
        ensurepip_path = Path(ensurepip_path.strip()) / "_bundled"
    except CalledProcessError:
        pass
    else:
        if ensurepip_path.is_dir():
            yield ensurepip_path

    # Standard wheels path
    wheels_dir = Path("/usr/share/python-wheels")
    if wheels_dir.exists():
        yield wheels_dir
