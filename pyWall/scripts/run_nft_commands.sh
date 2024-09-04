#!/bin/bash
if [ "$#" -eq 0 ]; then
  echo "Error con el numero de parametros en run_nft_commands.sh.."
else

  /usr/sbin/nft "$@"
fi