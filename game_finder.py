import winreg
import os
from typing import List

__all__ = ["get_bs_path"]


class NotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(*args, **kwargs)


def get_steam_path() -> str:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Valve\Steam") as key:
        return winreg.QueryValueEx(key, "SteamPath")[0]


def get_steam_collection() -> List[str]:
    steam_path = get_steam_path()
    result = [steam_path]
    with open(os.path.join(steam_path, "steamapps", "libraryfolders.vdf")) as f:
        for line in f:

            data = line.strip().replace("\\\\", "/").replace('"', "").split(maxsplit=1)
            if len(data) < 2:
                continue
            if data[0].isnumeric():
                result.append(data[1])
    return [os.path.join(path, "steamapps", "common") for path in result]


def get_bs_path():
    paths = get_steam_collection()
    bs_path = [os.path.join(path, "Beat Saber") for path in paths]
    for path in bs_path:
        if os.path.exists(path):
            return path
    raise NotFoundException("Game not found")
