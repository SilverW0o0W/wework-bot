#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/21
@brief:
"""

import time

import torndb


class NoticeWriter(object):
    def __init__(self, config):
        self.now = int(time.time())
        self.db = torndb.Connection(**config)

    def write_project(self, project):
        sql = """
        INSERT INTO `project`
        (`name`, `url`)
        VALUES 
        (%s, %s)
        """
        params = [project["name"], project["url"], ]
        return self.db.insert(sql, *params)

    def write_robot(self, robot):
        sql = """
        INSERT INTO `robot`
        (`name`, `webhook`)
        VALUES 
        (%s, %s)
        """
        params = [robot["name"], robot["webhook"], ]
        return self.db.insert(sql, *params)

    def write_notices(self, notices, created_time=None):
        created_time = created_time or int(time.time())
        notice_tuple = [
            (
                n["project_id"],
                n["robot_id"],
                n["type"],
                n["sub_type"],
                n["notice_time"],
                1,
                created_time,
                created_time,
            )
            for n in notices
        ]
        sql = """
        INSERT INTO `notice` 
        (`project_id`, `robot_id`, `type`, `sub_type`, `notice_time`, `status`, `created_time`, `updated_time`)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.insertmany(sql, notice_tuple)
