#!/bin/bash

# when called, find script directory and run everything except ourselves.
# http://mywiki.wooledge.org/BashFAQ/028
if [[ -s "$BASH_SOURCE" ]] && [[ -x "$BASH_SOURCE" ]]; then
        # we found ourselves, do the needful.
        source_dir=$(dirname $(readlink -f "$BASH_SOURCE"))
	self_name=$(basename $(readlink -f "$BASH_SOURCE"))
fi

# bail if unset
if [ -z "${source_dir}" ] ; then echo "failed to find self" 1>&2 ; exit 255 ; fi

echo "${self_name} running..."
echo -n "selinux context is "
id -Z

for file in "${source_dir}"/* ; do
  file=$(basename "${file}")
  case $file in
    ${self_name})
      # nop
      ;;
    *)
      ${source_dir}/${file}
      ;;
  esac
done
