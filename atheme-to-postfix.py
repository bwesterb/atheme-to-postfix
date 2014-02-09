#!/usr/bin/env python

""" Creates a postfix forwarding table ("virtual map" in postfix lingo) from the
    (nickserv) user database of the atheme IRC daemon.

    Return codes:

            0 Everything is fine

    Created by Bas Westerbaan <bas@westerbaan.name> """

import re
import sys
import os.path
import argparse

class Program:
    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description="Creates postfix virtual "
                    +"map from atheme's services.db")
        # TODO set a sane default
        parser.add_argument('--db', '-d', type=str,
                                metavar='PATH-TO-SERVICES.DB',
                                default='services.db',
                        help='Path to services.db')
        parser.add_argument('--domain', '-D', type=str,
                                metavar='DOMAIN',
                                default='domain.com',
                        help='Domain to create forward for')
        self.args = parser.parse_args()

    def __init__(self):
        self.email_re = re.compile(r'^[a-z0-9\.]+@[a-z0-9\.]+\.[a-z0-9\.]+$')
        self.nick_re = re.compile(r'^[a-z0-9]+$')

    def main(self, argv):
        self.parse_args(argv)
        nicks = self.load_services_db()
        self.print_map(nicks)

    def load_services_db(self):
        nicks = {}
        with open(self.args.db) as f:
            for lineno, l in enumerate(f):
                bits = l.split(' ', 5)
                if not bits:
                    print '# WARNING l.%s empty line' % lineno
                    continue
                if bits[0] != 'MU':
                    continue
                if len(bits) != 6:
                    print '# WARNING l.%s missing fields' % lineno
                    continue
                nick = bits[2].lower()
                email = bits[4].lower()
                if not self.nick_re.match(nick):
                    print '# WARNING l.%s invalid nick %s' % (
                            lineno, repr(nick))
                    continue
                if not self.email_re.match(email):
                    print '# WARNING l.%s invalid email %s' % (
                            lineno, repr(email))
                    continue
                if nick in nicks:
                    print '# WARNING l.%s double nick %s' % (
                            lineno, nick)
                    continue
                nicks[nick] = email
        return nicks

    def print_map(self, nicks):
        for nick, email in nicks.iteritems():
            print '%s@%s %s' % (nick, self.args.domain, email)

if __name__ == '__main__':
    sys.exit(Program().main(sys.argv))

# vim: sw=4 bs=2 ts=4 et
