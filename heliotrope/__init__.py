from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=5, minor=2, micro=0, releaselevel="final", serial=0)

__version__ = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
__detailed_version__ = f"{__version__}-{version_info.releaselevel}"
