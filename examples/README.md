atheme-to-postfix example scripts
=================================

This directory contains a couple of scripts that can be used
to extract the relevant lines from `services.db` and write them
to a file readable by another user. In this way, the Postfix
installation need not be on the same machine.

Contents
--------

* `alias-cron` can be used to periodically run an extraction of the needed
lines from `services.db`. These lines are written to a location that can be read
by a non-privileged user.
* `alias-login` can be used to give a non-privileged user access to the output
of `atheme-to-postfix.py`, for example, via SSH.

/ vim: sw=4 bs=2 ts=4 et tw=80
