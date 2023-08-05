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


class SubUserAccessKey(object):

    def __init__(self, accessKey=None, secretAccessKey=None, createTime=None, status=None, yn=None):
        """
        :param accessKey: (Optional) accessKey
        :param secretAccessKey: (Optional) secretAccessKey
        :param createTime: (Optional) 创建时间
        :param status: (Optional) 禁用/启用状态[0-禁用,1-启用]
        :param yn: (Optional) 删除/有效状态[0-删除,1-有效]
        """

        self.accessKey = accessKey
        self.secretAccessKey = secretAccessKey
        self.createTime = createTime
        self.status = status
        self.yn = yn
