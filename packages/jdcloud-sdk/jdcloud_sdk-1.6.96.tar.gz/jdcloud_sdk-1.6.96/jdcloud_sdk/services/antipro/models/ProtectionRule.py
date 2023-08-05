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


class ProtectionRule(object):

    def __init__(self, type=None, cleanThresholdBps=None, cleanThresholdPps=None, spoofIpEnable=None, srcNewConnLimitEnable=None, srcNewConnLimitValue=None, dstNewConnLimitEnable=None, dstNewConnLimitValue=None, datagramRangeMin=None, datagramRangeMax=None, geoBlackList=None, ipBlackList=None, ipWhiteList=None):
        """
        :param type: (Optional) 防护规则类型: 0: 默认防护包规则, 1: IP 自定义规则
        :param cleanThresholdBps: (Optional) 清洗触发值 bps
        :param cleanThresholdPps: (Optional) 清洗触发值 pps
        :param spoofIpEnable: (Optional) 虚假源开启
        :param srcNewConnLimitEnable: (Optional) 源新建连接限速开启
        :param srcNewConnLimitValue: (Optional) 源新建连接速率
        :param dstNewConnLimitEnable: (Optional) 目的新建连接开启
        :param dstNewConnLimitValue: (Optional) 目的新建连接速率
        :param datagramRangeMin: (Optional) 报文最小长度
        :param datagramRangeMax: (Optional) 报文最大长度
        :param geoBlackList: (Optional) geo 拦截地域列表
        :param ipBlackList: (Optional) IP 黑名单列表
        :param ipWhiteList: (Optional) IP 白名单列表
        """

        self.type = type
        self.cleanThresholdBps = cleanThresholdBps
        self.cleanThresholdPps = cleanThresholdPps
        self.spoofIpEnable = spoofIpEnable
        self.srcNewConnLimitEnable = srcNewConnLimitEnable
        self.srcNewConnLimitValue = srcNewConnLimitValue
        self.dstNewConnLimitEnable = dstNewConnLimitEnable
        self.dstNewConnLimitValue = dstNewConnLimitValue
        self.datagramRangeMin = datagramRangeMin
        self.datagramRangeMax = datagramRangeMax
        self.geoBlackList = geoBlackList
        self.ipBlackList = ipBlackList
        self.ipWhiteList = ipWhiteList
