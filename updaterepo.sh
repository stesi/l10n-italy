#!/usr/bin/env bash
cwd=$(pwd)
for f in ../repository/*; do
    if [ -d "$f" ]; then
        # Will not run if no directories are available
        #echo "$f"
        cd $f
#echo $(pwd)
        git pull
        git submodule update --init --remote stesi/l10n-italy
        git commit -am "Update l10n-italy"
        git push
        cd  "$cwd" 
    fi
done

