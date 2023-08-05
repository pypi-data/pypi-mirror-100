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


class ConfigUrlRuleRequest(JDCloudRequest):
    """
    URL改写配置
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(ConfigUrlRuleRequest, self).__init__(
            '/domain/{domain}/configUrlRule', 'POST', header, version)
        self.parameters = parameters


class ConfigUrlRuleParameters(object):

    def __init__(self, domain, ):
        """
        :param domain: 用户域名
        """

        self.domain = domain
        self.beforeRegex = None
        self.afterRegex = None

    def setBeforeRegex(self, beforeRegex):
        """
        :param beforeRegex: (Optional) url改写之前的正则表达式
        """
        self.beforeRegex = beforeRegex

    def setAfterRegex(self, afterRegex):
        """
        :param afterRegex: (Optional) url改写之后的正则表达式
        """
        self.afterRegex = afterRegex

