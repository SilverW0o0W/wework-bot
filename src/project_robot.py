#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/20
@brief:
"""
import time
import datetime
import json

import torndb
import requests


def get_0_hour_stamp(timestamp):
    date = datetime.date.fromtimestamp(timestamp)
    return int(time.mktime(date.timetuple()))


class ProjectRobot(object):
    def __init__(self):
        self.now = int(time.time())
        config = {
        }
        self.db = torndb.Connection(**config)

    def get_notices(self, start, end):
        sql = """
        SELECT
        n.id AS notice_id,
        n.type,
        n.sub_type,
        n.project_id,
        p.name AS project_name,
        p.url AS project_url,
        n.robot_id,
        r.webhook
        FROM notice n
        JOIN project p ON n.project_id = p.id
        JOIN robot r ON n.robot_id = r.id
        WHERE n.notice_time >= %s
        AND n.notice_time < %s
        AND n.status = 1
        """
        params = [start, end, ]
        return self.db.query(sql, *params)

    @staticmethod
    def get_content(notice_type, sub_type):
        notice_type_map = {
            1: "开发",
            2: "联调",
            3: "提测",
            4: "测试",
            5: "上线",
        }
        notice_sub_type_map = {
            1: "即将开始",
            2: "进行中",
            3: "即将结束",
        }
        return f"项目{notice_type_map[notice_type]}{notice_sub_type_map[sub_type]}，请关注。"

    def build_notice_content(self, notice):
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": notice["project_name"],
                        "description": self.get_content(notice["type"], notice["sub_type"]),
                        "url": notice["project_url"],
                        "picurl": ""
                    }
                ]
            }
        }

        return data

    @staticmethod
    def send_notice(webhook, content, is_json=True):
        response = requests.post(webhook, data=json.dumps(content) if is_json else content)
        return response

    def run(self):
        today = get_0_hour_stamp(self.now)
        tomorrow = today + 86400
        notices = self.get_notices(today, tomorrow)
        for notice in notices:
            content = self.build_notice_content(notice)
            self.send_notice(notice["webhook"], content)


def main():
    r = ProjectRobot()
    r.run()


if __name__ == '__main__':
    main()
