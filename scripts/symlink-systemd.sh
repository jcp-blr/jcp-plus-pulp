#!/bin/bash
for module in "jcp-plus-pulp-server" "jcp-plus-pulp-monitor-away" "jcp-plus-pulp-monitor-window-x11"; do
    ln -s $(pwd)/$module/misc/${module}.service ~/.config/systemd/user/${module}.service
done
