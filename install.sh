#!/usr/bin/env bash

set -u

VERSION=v1.0.0

function requirement()
{
  local cmd=$1

  if ! command -v "$cmd" &> /dev/null
  then
    echo "$cmd could not be found. install using \`sudo apt install $cmd\`"
    exit 127
  fi

}
function requirements()
{
  requirement python3
  requirement pip3
  requirement fzf
  requirement git 
}

function uninstall ()
{
  if [ -d "$HOME"/.pytermv ]; then
    rm -rf "$HOME"/.pytermv
  fi
  sed -i '/pytermv/d' "$HOME"/.bashrc
  echo 'Uninstall completed'
}

function install ()
{
  local new_install=false
  
  requirements

  if [ ! -d "$HOME"/.pytermv ]; then
    git clone https://github.com/Ahmed-Zamouche/pytermv.git "$HOME"/.pytermv
    echo "PATH=\"\$HOME/.pytermv:\$PATH\"" >> "$HOME"/.bashrc 
   new_install=true
  fi

  pushd "$HOME"/.pytermv || exit 1
  git fetch --all --tags
  git checkout "$VERSION"

  pip3 install --upgrade -r requirements.txt

  popd || exit 1
  
  if [[ $new_install = true ]]; then
    echo 'Install completed'
    echo 'Restart your shell `source ~/.bashrc`'
  fi


}

function version()
{
  echo "$VERSION"
}

function help()
{
    echo "Usage: ${0} [ -i | --install ]
               [ -u | --uninstall ]
               [ -v | --version ]
               [ -h | --help  ]"
}

SHORT=i,u,r,v,h
LONG=install,uninstall,requirements,version,help
OPTS=$(getopt -a -n player --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -i | --install )
      install
      break
      ;;
    -u | --uninstall )
      uninstall
      break
      ;;
    -r | --requirements )
      requirements
      break
      ;;
    -h | --help)
      help
      break
      ;;
    -v | --version)
      version
      break
      ;;
    *)
      echo "Unexpected option: $1"
      help
      exit 2
      ;;
  esac
done

exit 0






