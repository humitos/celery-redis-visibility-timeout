#!/bin/bash

if [ ! -e $HOME/.local/bin/uv ]; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    $HOME/.local/bin/uv venv
    $HOME/.local/bin/uv pip install 'celery[redis]==5.5.3'
fi

$HOME/.local/bin/uv run python3 -u /app/trigger.py
