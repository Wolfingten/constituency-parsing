#!/bin/sh

secret-tool lookup ssh lsv | sshpass -v rsync -aPuv /home/wolfingten/projects/constituency-parsing/* jguertler@contact.lsv.uni-saarland.de:/nethome/jguertler/constituency-parsing --exclude-from /home/wolfingten/projects/constituency-parsing/.gitignore

