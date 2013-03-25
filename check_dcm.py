#!/usr/bin/python
# 
# check_dcm.py
# Nagios/Icinga plugin to check DICOM services.
# 
# The script is a wrapper for dcmtk's (http://dicom.offis.de/dcmtk.php.en) echoscu
# to monitor STORE SCP.  It will have to be installed (or the binary built) on the
# nagios system. Easiest way on an ubuntu system is to use apt:
# 
# sudo apt-get install dcmtk
# 
# Usage:
# You can hard code your port/ae_title but I prefer to use object variables as below
# (http://nagios.sourceforge.net/docs/3_0/customobjectvars.html)
# 
# define command {
#         command_name    check_dcm
#         command_line    $USER1$/check_dcm -H $HOSTADDRESS$ -p $_HOSTPORT$ -a $_HOSTAE_TITLE$ -v
#         }


import subprocess
import sys
import argparse

# Version
VERSION = '0.1.0'

# Exit Codes
STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-V", "--version", action="store_true", help="display plugin version")
parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")
parser.add_argument("-t", "--timeout", default='10', help="seconds before request timeout")
parser.add_argument("-aet", "--aetitle", help="calling AE Title (default: ECHOSCU")
parser.add_argument("-aec", "--call", help="ae title of modality (default: ANY-SCP")
parser.add_argument("-H", "--hostname", help="hostname of modality")
parser.add_argument("-p", "--port", default='104', help="tcp/ip port number of modality")


try:
	args = parser.parse_args()
except SystemExit, e:
	# bad args, so service state unknown
	sys.exit(STATE_UNKNOWN)
	raise e

if args.version:
	# service state unknown, but here's your version number.
	print VERSION
	sys.exit(STATE_UNKNOWN)

# build command line arguments
cmd = ['/usr/bin/echoscu']

if args.verbosity >= 3:
	cmd.append('--debug')
elif args.verbosity == 2:
	cmd.append('--verbose')

if args.timeout:
	cmd.append('-to') 
	cmd.append(args.timeout)

if args.aetitle:
	cmd.append('-aet')
	cmd.append(args.aetitle)

if args.call:
	cmd.append('-aec')
	cmd.append(args.call)

cmd.append(args.hostname)
cmd.append(args.port)

# send out a dicom ping and see what comes back
try:
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
except Exception, e:
	sys.exit(STATE_UNKNOWN)
else:
	stdout = p.communicate()[0]

	if p.returncode:
		if args.verbosity:
			print "CRITICAL - Association Request Failed (TCP Initialization Error: Connection refused)"
			if args.verbosity > 1:
				for line in stdout.splitlines():
					print line
		else:
			print "CRITICAL - Association Request Failed"

		sys.exit(STATE_CRITICAL)

	else:
		if args.verbosity:
			print "OK - Association Accepted (Received Echo Response (Status: Success))"
			if args.verbosity > 1:
				for line in stdout.splitlines():
					print line
		else:
			print "OK - Association Accepted"

		sys.exit(STATE_OK)



