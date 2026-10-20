#!/bin/bash
# The old launcher has been retired. Use the backed-up theme migration.
set -euo pipefail
exec bash "$(dirname "$0")/install-theme.sh"
