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


class DescribeAlarmsRequest(JDCloudRequest):
    """
    查询规则列表
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(DescribeAlarmsRequest, self).__init__(
            '/groupAlarms', 'GET', header, version)
        self.parameters = parameters


class DescribeAlarmsParameters(object):

    def __init__(self, ):
        """
        """

        self.pageNumber = None
        self.pageSize = None
        self.serviceCode = None
        self.product = None
        self.dimension = None
        self.ruleName = None
        self.ruleType = None
        self.enabled = None
        self.ruleStatus = None
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
        :param product: (Optional) 产品标识，如redis下分多个产品(redis2.8cluster、redis4.0)。同时指定serviceCode与product时，product优先生效
        """
        self.product = product

    def setDimension(self, dimension):
        """
        :param dimension: (Optional) 产品下的维度标识，指定dimension时必须指定product
        """
        self.dimension = dimension

    def setRuleName(self, ruleName):
        """
        :param ruleName: (Optional) 规则名称
        """
        self.ruleName = ruleName

    def setRuleType(self, ruleType):
        """
        :param ruleType: (Optional) 规则类型, 1表示资源监控，6表示站点监控,7表示可用性监控
        """
        self.ruleType = ruleType

    def setEnabled(self, enabled):
        """
        :param enabled: (Optional) 规则状态：1为启用，0为禁用
        """
        self.enabled = enabled

    def setRuleStatus(self, ruleStatus):
        """
        :param ruleStatus: (Optional) 资源的规则状态  2：报警、4：数据不足
        """
        self.ruleStatus = ruleStatus

    def setFilters(self, filters):
        """
        :param filters: (Optional) 服务码或资源Id列表
products - 产品product，精确匹配，支持多个
resourceIds - 资源Id，精确匹配，支持多个（必须指定serviceCode、product或dimension，否则该参数不生效）
alarmIds - 规则id，精确匹配，支持多个
        """
        self.filters = filters

