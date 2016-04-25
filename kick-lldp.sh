#!/bin/bash

SKIP_INTERFACES=

if [ -f /etc/px-firstboot/lldp.config ] ; then
  . /etc/px-firstboot/lldp.config
fi

# first, start lldp
#systemctl start lldapd.service

# next, walk the interfaces
for intf in /sys/class/net/* ; do
  face=$(basename "${intf}")
  # check is we flagged a skip
  case "${SKIP_INTERFACES}" in
    *${face}*)
      continue
      ;;
  esac

  # check if a virtual interface
  dest=$(readlink "${intf}")
  case "${dest}" in
    *virtual*)
      continue
      ;;
  esac

  # check if wireless
  if [ -e "${intf}/phy80211" ] ; then
    continue
  fi

  # bop lldp
  lldptool set-lldp -i "${face}" -g nb adminStatus=rxtx
  lldptool set-tlv -i "${face}" -g nb -V sysName -c enableTx=yes
done
