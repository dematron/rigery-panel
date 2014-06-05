#!/usr/bin/env python
# coding=utf-8

__author__ = 'iLiKo'

"""
Return disk usage statistics about the given path as a (total, used, free).
Values are expressed in bytes.
"""

import os
import collections

def get_linux_disk_usage(path):
    if hasattr(os, 'statvfs'):  # POSIX
        linux_diskusage = collections.namedtuple('usage', 'total used free')
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return linux_diskusage(total, used, free)
    else:
        raise NotImplementedError("platform not supported")

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

# Usage example
if __name__ == '__main__':
    # Enter something like - "/" (with out ")
    path = raw_input("Enter the Volume path: ")
    usage = get_linux_disk_usage(path)
    print "HDD usage: Total: %s, Used: %s, Free: %s" % (bytes2human(usage.total), bytes2human(usage.used),
                                                        bytes2human(usage.free))