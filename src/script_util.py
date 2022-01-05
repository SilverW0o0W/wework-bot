#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/1/5
@brief:
"""

import toml


def load_toml_config(config_path):
    with open(config_path, "r") as f:
        config = toml.load(f)
    return config
