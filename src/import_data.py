#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/21
@brief:
"""

import sys

import build_util
import script_util
from notice_writer import NoticeWriter

test_data = {
    "project": {
        "name": "",
        "url": "",
    },
    "schedule": {
        "开发": "2022-01-06",
        "联调": "2022-01-12",
        "提测": "2022-01-14",
        "测试": "",
        "上线": "2022-01-26",
    },
    "notice": {
        "before": [1, 2, 3, 4, 5, ],
        "start": [1, 2, 3, 4, 5, ],
    },
    "robot_id": 1,
}


def run(config, data):
    writer = NoticeWriter(config)
    project_id, msg = writer.write_project(data["project"])
    robot_id, _ = (data["robot_id"], "") if data.get("robot_id") else writer.write_robot(data["robot"])
    schedule_date = build_util.get_schedule_date(data["schedule"])
    notices = build_util.build_notices_from_schedule(project_id, robot_id, schedule_date, data["notice"])
    writer.write_notices(notices)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Params error. python import_data.py [config_path]")
        exit(1)

    toml_config = script_util.load_toml_config(sys.argv[1])
    run(toml_config["BOT_DB"], test_data)
