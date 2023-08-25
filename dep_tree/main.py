import platform
import urllib.request
import os
import subprocess
import sys
import os.path as path
import tarfile
import shutil

BIN = path.join(path.dirname(__file__), 'dep-tree')
BIN_TAR = BIN+'.tar.gz'
BIN_EXTRACTED = BIN+'-extracted'
__version__ = '0.13.4'

ARCH_OS_2_URL = {
    'Darwin': {
        'x86_64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_darwin_amd64.tar.gz",
        'arm64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_darwin_arm64.tar.gz",
        'aarch64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_darwin_arm64.tar.gz"
    },
    'Linux': {
        'x86_64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_linux_amd64.tar.gz",
        'arm64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_linux_arm64.tar.gz",
        'aarch64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_linux_arm64.tar.gz",
    },
    'Windows': {
        'x86_64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_windows_amd64.tar.gz",
        'AMD64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_darwin_amd64.tar.gz",
        'arm64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_windows_arm64.tar.gz",
        'aarch64': f"https://github.com/gabotechs/dep-tree/releases/download/v{__version__}/dep-tree_{__version__}_windows_arm64.tar.gz",
    },
}


def main():
    arch = platform.machine()
    system = platform.system()
    if system not in ARCH_OS_2_URL:
        print(f'Operating system "{system}" is not supported, supported operating systems are ${", ".join(ARCH_OS_2_URL.keys())}')

        exit(1)
    if arch not in ARCH_OS_2_URL[system]:
        print(f'Architecture "{arch}" for operating system "{system}" is not supported, supported architectures are ${", ".join(ARCH_OS_2_URL[system].keys())}')
        exit(1)

    if not path.isfile(BIN):
        if path.isdir(BIN_EXTRACTED):
            shutil.rmtree(BIN_EXTRACTED)
        if path.isfile(BIN_TAR):
            os.remove(BIN_TAR)
        urllib.request.urlretrieve(ARCH_OS_2_URL[system][arch], BIN_TAR)
        file = tarfile.open(BIN_TAR)
        file.extractall(BIN_EXTRACTED)
        shutil.move(path.join(BIN_EXTRACTED, 'dep-tree'), BIN)
        shutil.rmtree(BIN_EXTRACTED)
        os.remove(BIN_TAR)

    exit(subprocess.call(
        [BIN, *sys.argv[1:]],
        executable=BIN,
        stdout=sys.stdout.buffer,
        stderr=sys.stderr.buffer,
    ))

if __name__ == '__main__':
    main()
