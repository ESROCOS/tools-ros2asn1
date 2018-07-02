#!/usr/bin/env python2

# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import sys
import getopt
import errno
from ros2asn1 import ros2asn1


def main():
    outdir = parse_args()
    ros2asn1.process_all_messages(outdir)


def parse_args():
    '''
    Parse command-line arguments
    :returns outdir_asn: output directory for ASN.1 files
    '''
    inputfile = ''
    outdir_asn = ''
    try:
        args = sys.argv[1:]
        optlist, args = getopt.gnu_getopt(
            args,
            'h',
            ['help'])
    except:
        usage()
        sys.exit(errno.EINVAL)
    
    for opt, arg in optlist:
        if opt == '-h':
            usage()
            sys.exit(0)

    if len(args) == 1:
        outdir_asn = args[0]
    else:
        usage()
        sys.exit(errno.EINVAL)

    return outdir_asn


def usage():
    '''
    Print command-line usage
    '''
    print('Usage: {} <outdir-asn>'.format(sys.argv[0]))


if __name__ == "__main__":
    main()
