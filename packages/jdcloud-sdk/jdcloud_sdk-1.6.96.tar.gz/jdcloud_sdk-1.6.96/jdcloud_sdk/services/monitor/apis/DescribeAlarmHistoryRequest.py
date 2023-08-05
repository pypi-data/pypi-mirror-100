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

from jdcloud_sdk.core.jdcloudrequest import JDCloudRequest


class DescribeAlarmHistoryRequest(JDCloudRequest):
    """
    查询报警历史
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DescribeAlarmHistoryRequest, self).__init__(
            '/groupAlarmsHistory', 'GET', header, version)
        self.parameters = parameters


class DescribeAlarmHistoryParameters(object):

    def __init__(self, ):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.serviceCode = None
        self.product = None
        self.dimension = None
        self.region = None
        self.isAlarming = None
        self.status = None
        self.startTime = None
        self.endTime = None
        self.ruleType = None
        self.ruleName = None
        self.filters = None

    def setPageNumber(self, pageNumber):
        """
        :param pageNumber: (Optional) 当前所在页，默认为1
        """
        self.pageNumber = pageNumber

    def setPageSize(self, pageSize):
        """
        :param pageSize: (Optional) 页面大小，默认为20；取值范围[1, 100]
        """
        self.pageSize = pageSize

    def setServiceCode(self, serviceCode):
        """
        :param serviceCode: (Optional) 产品线标识，同一个产品线下可能存在多个product，如(redis下有redis2.8cluster、redis4.0)
        """
        self.serviceCode = serviceCode

    def setProduct(self, product):
        """
        :param product: (Optional) 产品标识,默认返回该product下所有dimension的数据。eg:product=redis2.8cluster（redis2.8cluster产品下包含redis2.8-shard与redis2.8-proxy、redis2.8-instance多个维度)。
        """
        self.product = product

    def setDimension(self, dimension):
        """
        :param dimension: (Optional) 维度标识、指定该参数时，查询只返回该维度的数据。如redis2.8cluster下存在实例、分片等多个维度
        """
        self.dimension = dimension

    def setRegion(self, region):
        """
        :param region: (Optional) 根据region筛选对应region的资源的报警历史
        """
        self.region = region

    def setIsAlarming(self, isAlarming):
        """
        :param isAlarming: (Optional) 正在报警, 取值为1
        """
        self.isAlarming = isAlarming

    def setStatus(self, status):
        """
        :param status: (Optional) 报警的状态,1为报警恢复、2为报警、4为报警恢复无数据
        """
        self.status = status

    def setStartTime(self, startTime):
        """
        :param startTime: (Optional) 开始时间
        """
        self.startTime = startTime

    def setEndTime(self, endTime):
        """
        :param endTime: (Optional) 结束时间
        """
        self.endTime = endTime

    def setRuleType(self, ruleType):
        """
        :param ruleType: (Optional) 规则类型,默认查询1， 1表示资源监控，6表示站点监控,7表示可用性监控
        """
        self.ruleType = ruleType

    def setRuleName(self, ruleName):
        """
        :param ruleName: (Optional) 规则名称模糊搜索
        """
        self.ruleName = ruleName

    def setFilters(self, filters):
        """
        :param filters: (Optional) serviceCodes - 产品线servicecode，精确匹配，支持多个
resourceIds - 资源Id，精确匹配，支持多个（必须指定serviceCode才会在该serviceCode下根据resourceIds过滤，否则该参数不生效）
alarmIds - 规则Id，精确匹配，支持多个
        """
        self.filters = filters

