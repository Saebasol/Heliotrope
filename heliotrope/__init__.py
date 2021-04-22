from collections import namedtuple

__version__ = "4.0.0-rc"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(
    major=4, minor=0, micro=0, releaselevel="candidate", serial=0
)
