#!/bin/bash

FILEPATH=$(readlink -f "canvas-cli")

chmod +x canvas-cli

ln -s $FILEPATH $HOME/.local/bin

echo Make sure $HOME/.local/bin is in your PATH.
