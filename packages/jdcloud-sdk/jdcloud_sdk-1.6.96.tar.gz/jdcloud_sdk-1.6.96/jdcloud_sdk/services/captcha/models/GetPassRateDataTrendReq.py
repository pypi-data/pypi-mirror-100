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


class GetPassRateDataTrendReq(object):

    def __init__(self, start, end, appIds=None, sceneIds=None):
        """
        :param start:  开始时间戳，单位秒，时间间隔要求大于5分钟，小于30天
        :param end:  结束时间戳，单位秒，时间间隔要求大于5分钟，小于30天
        :param appIds: (Optional) 应用id
        :param sceneIds: (Optional) 场景id
        """

        self.start = start
        self.end = end
        self.appIds = appIds
        self.sceneIds = sceneIds
