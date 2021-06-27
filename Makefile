prefix = /usr/local
BASEDIR = /opt/wlanpi-chat-bot

all:
	: # do nothing

install:
	mkdir -p $(DESTDIR)$(BASEDIR)
	cp -rf $(filter-out debian Makefile $^,$(wildcard *)) $(DESTDIR)$(BASEDIR)
	mkdir -p $(DESTDIR)/lib/systemd/system
	install -p -m 644 scripts/wlanpi-chat-bot.service $(DESTDIR)/lib/systemd/system

clean:
	: # do nothing

distclean: clean

uninstall:
	-rm -rf $(DESTDIR)$(BASEDIR)
	-rm -rf $(DESTDIR)/lib/systemd/system/wlanpi-chat-bot.service

.PHONY: all install clean distclean uninstall
