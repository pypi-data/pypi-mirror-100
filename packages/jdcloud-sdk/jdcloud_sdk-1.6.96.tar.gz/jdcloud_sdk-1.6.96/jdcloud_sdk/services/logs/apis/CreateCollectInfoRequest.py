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


class CreateCollectInfoRequest(JDCloudRequest):
    """
    创建采集配置，支持基于云产品模板生成采集模板；支持用于自定义采集配置。
    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateCollectInfoRequest, self).__init__(
            '/regions/{regionId}/logtopics/{logtopicUID}/collectinfos', 'POST', header, version)
        self.parameters = parameters


class CreateCollectInfoParameters(object):

    def __init__(self, regionId, logtopicUID, enabled, appCode, serviceCode, resourceType, ):
        """
        :param regionId: 地域 Id
        :param logtopicUID: 日志主题 UID
        :param enabled: 采集状态，0-禁用，1-启用
        :param appCode: 日志来源，只能是 custom/jdcloud
        :param serviceCode: 产品线,当日志来源为jdcloud时，必填
        :param resourceType: 采集实例类型, 只能是 all/part  当选择all时，传入的实例列表无效；custom类型的采集配置目前仅支持part方式，即用户指定实例列表；
        """

        self.regionId = regionId
        self.logtopicUID = logtopicUID
        self.enabled = enabled
        self.appCode = appCode
        self.serviceCode = serviceCode
        self.resourceType = resourceType
        self.resources = None
        self.templateUID = None
        self.logPath = None
        self.logFile = None
        self.logFilters = None
        self.filterEnabled = None

    def setResources(self, resources):
        """
        :param resources: (Optional) 采集实例列表：jdcloud类型最多添加20个资源；custom类型支持的资源数量不限；
        """
        self.resources = resources

    def setTemplateUID(self, templateUID):
        """
        :param templateUID: (Optional) 日志类型。当appcode为jdcloud时为必填
        """
        self.templateUID = templateUID

    def setLogPath(self, logPath):
        """
        :param logPath: (Optional) 日志路径。当appcode为custom时为必填。目前仅支持对 Linux 云主机上的日志进行采集，路径支持通配符“*”和“？”，文件路径应符合 Linux 的文件路径规则
        """
        self.logPath = logPath

    def setLogFile(self, logFile):
        """
        :param logFile: (Optional) 日志文件名。当appcode为custom时为必填。日志文件名支持正则表达式。
        """
        self.logFile = logFile

    def setLogFilters(self, logFilters):
        """
        :param logFilters: (Optional) 过滤器。设置过滤器后可根据用户设定的关键词采集部分日志，如仅采集 Error 的日志。目前最大允许5个。
        """
        self.logFilters = logFilters

    def setFilterEnabled(self, filterEnabled):
        """
        :param filterEnabled: (Optional) 过滤器是否启用。当appcode为custom时必填
        """
        self.filterEnabled = filterEnabled

