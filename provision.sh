#!/usr/bin/env bash
# Launcher for provision.py on Linux and macOS.
#   ./provision.sh devices
#   ./provision.sh install
#   ./provision.sh restore --wipe-media
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    py=python3
elif command -v python >/dev/null 2>&1; then
    py=python
else
    echo "Python 3.11 or newer is required but was not found." >&2
    echo "  Debian/Ubuntu: sudo apt install python3" >&2
    echo "  Fedora:        sudo dnf install python3" >&2
    exit 1
fi

if [ "$#" -eq 0 ]; then
    exec "$py" "$here/provision.py" install
fi
exec "$py" "$here/provision.py" "$@"
