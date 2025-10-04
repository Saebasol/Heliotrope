from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(
    major=7, minor=0, micro=0, releaselevel="candidate", serial=6
)

__version__ = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

if version_info.releaselevel != "final":
    __version__ = f"{__version__}-{version_info.releaselevel}.{version_info.serial}"
