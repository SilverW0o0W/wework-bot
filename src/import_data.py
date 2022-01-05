#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/21
@brief:
"""

import sys
import toml

import build_util
from notice_writer import NoticeWriter

test_data = {
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
    "robot_id": 1,
}


def load_config(config_path):
    with open(config_path, "r") as f:
        config = toml.load(f)
    return config


def run(config, data):
    writer = NoticeWriter(config)
    project_id = writer.write_project(data["project"])
    robot_id = data["robot_id"] if data.get("robot_id") else writer.write_robot(data["robot"])
    schedule_date = build_util.get_schedule_date(data["schedule"])
    notices = build_util.build_notices_from_schedule(project_id, robot_id, schedule_date, data["notice"])
    writer.write_notices(notices)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Params error. python import_data.py [config_path]")
        exit(1)

    toml_config = load_config(sys.argv[1])
    run(toml_config, test_data)
