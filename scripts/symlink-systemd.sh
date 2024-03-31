#!/bin/bash
for module in "aw-server" "jcp-plus-pulp-capture-away" "jcp-plus-pulp-capture-x11"; do
    ln -s $(pwd)/$module/misc/${module}.service ~/.config/systemd/user/${module}.service
done
