# coding=utf8

# Copyright 2018 JDCLOUD.COM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This class is auto generated by the jdcloud code generator program.


class SystemDisk(object):

    def __init__(self, category=None, diskSize=None, description=None):
        """
        :param category: (Optional) 否  系统盘的磁盘种类
        :param diskSize: (Optional) 系统盘大小
        :param description: (Optional) 系统盘描述
        """

        self.category = category
        self.diskSize = diskSize
        self.description = description
