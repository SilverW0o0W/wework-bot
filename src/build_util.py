#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2021/12/20
@brief:
"""

import time

import datetime

SCHEDULE_NAME_TO_TYPE = {
    "开发": 1,
    "联调": 2,
    "提测": 3,
    "测试": 4,
    "上线": 5,
}

SCHEDULE_NAME_TO_SUB_TYPE = {
    "before": 1,
    "start": 2,
    "end": 3,
}


def get_0_hour_stamp(timestamp):
    date = datetime.date.fromtimestamp(timestamp)
    return int(time.mktime(date.timetuple()))


def build_project(project):
    return project


def build_robot(robot):
    return robot


def get_schedule_date(schedule):
    schedule_date = {}
    for name, str_date in schedule.items():
        schedule_type = SCHEDULE_NAME_TO_TYPE.get(name)
        if not schedule_type or not str_date:
            continue
        schedule_date[schedule_type] = datetime.datetime.strptime(str_date, "%Y-%m-%d")
    return schedule_date


def build_notices_from_schedule(project_id, robot_id, schedule_date, notice):
    db_notice_list = []

    for schedule_sub_type_name, notice_schedule_types in notice.items():
        schedule_sub_type = SCHEDULE_NAME_TO_SUB_TYPE.get(schedule_sub_type_name)
        if not schedule_sub_type:
            continue
        notices = build_notices_from_sub_type(
            schedule_sub_type, notice_schedule_types, schedule_date, project_id, robot_id)
        db_notice_list.extend(notices)
    return db_notice_list


def build_notices_from_sub_type(schedule_sub_type, notice_schedule_types, schedule_date, project_id, robot_id):
    db_notices = []
    if schedule_sub_type not in (1, 2):
        return db_notices

    now = int(time.time())
    today = get_0_hour_stamp(now)
    for schedule_type in notice_schedule_types:
        # 跳过未输入排期
        if schedule_type not in schedule_date:
            continue

        notice_start_date = schedule_date[schedule_type]
        notice_time = get_notice_time_from_schedule_sub_type(schedule_sub_type, notice_start_date)
        if today >= notice_time:
            continue
        db_notice = build_db_notice(project_id, robot_id, schedule_type, schedule_sub_type, notice_time)
        db_notices.append(db_notice)
    return db_notices


def get_notice_time_from_schedule_sub_type(schedule_sub_type, start_date):
    if schedule_sub_type not in (1, 2):
        return 0
    if schedule_sub_type == 2:
        return int(start_date.timestamp())
    elif schedule_sub_type == 1:
        return int(start_date.timestamp()) - 86400
    return 0


def build_db_notice(project_id, robot_id, schedule_type, schedule_sub_type, notice_time):
    return {
        "project_id": project_id,
        "robot_id": robot_id,
        "type": schedule_type,
        "sub_type": schedule_sub_type,
        "notice_time": notice_time,
    }
