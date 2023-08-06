# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import configparser
from dataclasses import dataclass


@dataclass
class GiteeConfig:
    access_token: str


def load_config(filename) -> GiteeConfig:
    if not os.path.exists(filename):
        raise Exception('configuration file "%s" not found.' % filename)

    config = configparser.ConfigParser()
    config.read(filename)

    return GiteeConfig(
        access_token=config.get('auth', 'access_token')
    )
