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


class CCProtectionDefaultConfig(object):

    def __init__(self, ccThreshold=None, hostQps=None, hostUrlQps=None, ipHostQps=None, ipHostUrlQps=None):
        """
        :param ccThreshold: (Optional) HTTP 请求数阈值
        :param hostQps: (Optional) Host 的防护阈值
        :param hostUrlQps: (Optional) Host + Url 的防护阈值
        :param ipHostQps: (Optional) 每个源 IP 对 Host 的防护阈值
        :param ipHostUrlQps: (Optional) 每个源 IP 对 Host + Url 的防护阈值
        """

        self.ccThreshold = ccThreshold
        self.hostQps = hostQps
        self.hostUrlQps = hostUrlQps
        self.ipHostQps = ipHostQps
        self.ipHostUrlQps = ipHostUrlQps
