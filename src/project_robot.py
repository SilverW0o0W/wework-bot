#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/20
@brief:
"""
import sys
import time
import datetime
import json

import requests

import script_util
import sqlalchemy_util


def get_0_hour_stamp(timestamp):
    date = datetime.date.fromtimestamp(timestamp)
    return int(time.mktime(date.timetuple()))


class ProjectRobot(object):
    def __init__(self, config):
        self.now = int(time.time())
        uri = sqlalchemy_util.build_db_uri(config)
        self.engine = sqlalchemy_util.init_engine(uri)

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
        params = (start, end,)
        with sqlalchemy_util.Connection(self.engine) as conn:
            return conn.read_list(sql, params)

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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Params error. python project_robot.py [config_path]")
        exit(1)

    toml_config = script_util.load_toml_config(sys.argv[1])
    r = ProjectRobot(toml_config["BOT_DB"])
    r.run()
