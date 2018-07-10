#!/bin/bash

function usage() {
  echo "encode [-l lame_args] [-f ffmpeg_args] -i input -o output"
}

#
# Parse command line arguments

while getopts "i:o:l:f:h" arg; do
  case $arg in
    i)
      INPUT=${OPTARG}
      ;;
    o)
      OUTFILE=${OPTARG}
      ;;
    l)
      LAME_ARGS=${OPTARG}
      ;;
    f)
      FFMPEG_ARGS=${OPTARGS}
      ;;      
    h)
      usage
      exit 0
      ;;
  esac
done

if [[ -z ${INPUT+x} ]]; then
  usage
  exit 1
fi

if [[ -z ${OUTFILE+x} ]]; then
  usage
  exit 2
fi

TMPFILE=$(mktemp -p /tmp tmp.XXXX.mp3)

#
# extract the audio from the video file
eval "ffmpeg -i \"${INPUT}\" -vn -acodec libmp3lame -ar 44100 -ac 2 -ab 128000 ${FFMPEG_ARGS} ${TMPFILE}"

#
# rename and encode some meta-data (in LAME_ARGS) in the
# file.
eval "lame --mp3input ${LAME_ARGS} ${TMPFILE} ${OUTFILE}"

# remove the temporary file.
rm $TMPFILE

unset TMPFILE

