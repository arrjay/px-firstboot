install: px-firstboot.service startup.sh kick-lldp.sh
	# directories
	-install -d -m 0755 $(ROOT)/etc/px-firstboot
	-install -d -m 0755 $(ROOT)/lib/systemd/system
	-install -d -m 0755 $(ROOT)/usr/share/doc/px-firstboot
	-install -d -m 0755 $(ROOT)/var/lib/px-firstboot
	-install -d -m 0755 $(ROOT)/usr/libexec/px-firstboot
	# docs
	install -m 0644 LICENSE $(ROOT)/usr/share/doc/px-firstboot
	# systemd
	install -m 0644 px-firstboot.service $(ROOT)/lib/systemd/system/px-firstboot.service
	# init-kick
	install -m 0755 startup.sh $(ROOT)/usr/libexec/px-firstboot/startup
	# lldp
	install -m 0755 kick-lldp.sh $(ROOT)/usr/libexec/px-firstboot/lldp
