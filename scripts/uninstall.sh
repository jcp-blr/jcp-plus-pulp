#!/bin/bash

modules=$(pip3 list --format=legacy | grep 'jcp-plus-pulp-' | grep -o '^jcp-plus-pulp-[^ ]*')

for module in $modules; do
    pip3 uninstall -y $module
done

