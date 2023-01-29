#!/usr/bin/env bash

MPV_FLAGS=${MPV_FLAGS:---no-resume-playback}
MPV_FULL_SCREEN=${MVP_FULL_SCREEN:-}
TERM_SWALLOW=${TERM_SWALLOW:-false}
MPV_BG=${MPV_BG:-false}


_play() {
    printf '%s\n' "Fetching channel, please wait..."
    
    IFS=$'\t'; channel=( ${1} )

    if [ "${TERM_SWALLOW}" = true ]; then
        WID=$(xdo id)
        xdo hide
        # shellcheck disable=SC2086
        mpv "${channel[4]}" ${MPV_FLAGS} "${MPV_FULL_SCREEN}" --force-media-title="\"${channel[0]}\"" --force-window=immediate
        xdo show "$WID" && xdo activate "$WID"
    else
        # shellcheck disable=SC2086
        mpv "${channel[4]}" "${MPV_FLAGS}" "${MPV_FULL_SCREEN}" --force-media-title="\"${channel[0]}\""
    fi
}

_playbg() {
    IFS=$'\t'; channel=( ${1} )
    { setsid -f mpv "${channel[4]}" "${MPV_FLAGS}" "${MPV_FULL_SCREEN}" --force-media-title="\"${channel[0]}\"" --force-window=immediate >/dev/null 2>&1 ; }
}

help()
{
    echo "Usage: ${0} [ -b | --background ]
               [ -f | --full-screen ]
               [ -s | --term-swallo ]
               [ -a | --args ]
               [ -h | --help  ]"
    exit 2
}

SHORT=b,f,s,a:,h
LONG=background,full-screen,term-swallo,flags:,help
OPTS=$(getopt -a -n player --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -b | --background )
      MPV_BG=true
      shift 1
      ;;
    -f | --full-screen )
      MPV_FULL_SCREEN=--fs
      shift 1
      ;;
    -s | --term-swallo )
      TERM_SWALLOW=true
      shift 1
      ;;
    -a | --flags )
      MPV_FLAGS="$2"
      shift 2
      ;;
    -h | --help)
      help
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      help
      ;;
  esac
done

if [ "${MPV_BG}" = true ]; then
  _playbg "${1}"
else
  _play "${1}"
fi
