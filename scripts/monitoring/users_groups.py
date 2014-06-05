#!/usr/bin/env python
# coding=utf-8

__author__ = 'iLiKo'

import pwd
import grp
import operator
from collections import OrderedDict

def get_users():
    # Load all of the user data, sorted by username
    all_user_data = pwd.getpwall()
    interesting_users = sorted((u
                                for u in all_user_data
                                if not u.pw_name.startswith('_')),
                               key=operator.attrgetter('pw_name'))

    # Return the data
    users = {}
    for u in interesting_users:
        users[u.pw_name] = u.pw_name, u.pw_uid, u.pw_dir, u.pw_gecos
    return users

def get_groups():
    # Load all of the user data, sorted by username
    all_groups = grp.getgrall()
    interesting_groups = sorted((g
                                 for g in all_groups
                                 if not g.gr_name.startswith('_')),
                                key=operator.attrgetter('gr_name'))
    # Return the data
    groups = {}
    for g in interesting_groups:
        groups[g.gr_name] = g.gr_gid
    return groups

def get_all_group_members(gid):
    primary_members = [user.pw_name for user in pwd.getpwall() if user.pw_gid == gid]
    additional_members = grp.getgrgid(gid).gr_mem
    members = primary_members + additional_members
    group_members = list(OrderedDict.fromkeys(members))
    return {"group_members": group_members}

# Use of dictionary get_group_info()
# get_groups().keys() - groups
# get_groups()['GROUP'] - GID


# Use of dictionary get_users()
# get_users().keys() - users
# get_users()['USERNAME'] - user info
# get_users()['USERNAME'][0-3] - User, UID, Home Dir, Description

if __name__=="__main__":
    print get_groups()
    print get_users()
    print get_all_group_members(0)
