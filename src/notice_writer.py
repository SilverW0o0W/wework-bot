#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/21
@brief:
"""

import time

import torndb
import build_util


class NoticeWriter(object):
    def __init__(self):
        self.now = int(time.time())
        config = {
        }
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

    def run(self):
        data = {
            "project": {
                "name": "",
                "url": "",
            },
            "schedule": {
                "开发": "2021-11-08",
                "联调": "2021-12-30",
                "提测": "2022-1-5",
                "测试": "",
                "上线": "2022-1-14",
            },
            "notice": {
                "before": [1, 2, 3, 4, 5, ],
                "start": [1, 2, 3, 4, 5, ],
            },
            "robot_id": 0,
            "robot": {
                "name": "",
                "webhook": ""
            }
        }
        project_id = self.write_project(data["project"])
        robot_id = self.write_robot(data["robot"])
        schedule_date = build_util.get_schedule_date(data["schedule"])
        notices = build_util.build_notices_from_schedule(project_id, robot_id, schedule_date, data["notice"])
        self.write_notices(notices)


def main():
    w = NoticeWriter()
    w.run()


if __name__ == '__main__':
    main()
