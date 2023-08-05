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


class CreateClusterRequest(JDCloudRequest):
    """
    - 创建集群
- 证书
  - 关于kubernetes的证书，默认生成，不需要用户传入。
- nodegroup
  - cluster必须与nodeGroup进行绑定
  - cluster支持多nodegroup
  - 状态
    - pending,reconciling,deleting状态不可以操作更新接口
    - running，running_with_error状态可以操作nodegroup所有接口
    - error状态只可以查询，删除
    - delete状态的cluster在十五分钟内可以查询，十五分钟后无法查询到
- 状态限制
  - pending,reconciling,deleting状态不可以操作更新接口
  - running状态可以操作cluster所有接口
  - error状态只可以查询，删除
  - delete状态的cluster在十五分钟内可以查询，十五分钟后无法查询到

    """

    def __init__(self, parameters, header=None, version="v1"):
        super(CreateClusterRequest, self).__init__(
            '/regions/{regionId}/clusters', 'POST', header, version)
        self.parameters = parameters


class CreateClusterParameters(object):

    def __init__(self, regionId, name, azs, nodeGroup, masterCidr, accessKey, secretKey, ):
        """
        :param regionId: 地域 ID
        :param name: 名称（同一用户的 cluster 允许重名）
        :param azs: 集群所在的az
        :param nodeGroup: 集群节点组
        :param masterCidr: k8s的master的cidr
        :param accessKey: 用户的AccessKey，插件调用open-api时的认证凭证
        :param secretKey: 用户的SecretKey，插件调用open-api时的认证凭证
        """

        self.regionId = regionId
        self.name = name
        self.description = None
        self.basicAuth = None
        self.clientCertificate = None
        self.version = None
        self.azs = azs
        self.nodeGroup = nodeGroup
        self.masterCidr = masterCidr
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.userMetrics = None
        self.addonsConfig = None

    def setDescription(self, description):
        """
        :param description: (Optional) 描述
        """
        self.description = description

    def setBasicAuth(self, basicAuth):
        """
        :param basicAuth: (Optional) 默认开启 basicAuth与clientCertificate最少选择一个
        """
        self.basicAuth = basicAuth

    def setClientCertificate(self, clientCertificate):
        """
        :param clientCertificate: (Optional) 默认开启 clientCertificate
        """
        self.clientCertificate = clientCertificate

    def setVersion(self, version):
        """
        :param version: (Optional) kubernetes的版本
        """
        self.version = version

    def setUserMetrics(self, userMetrics):
        """
        :param userMetrics: (Optional) deprecated 在addonsConfig中同时指定，将被addonsConfig的设置覆盖 <br>是否启用用户自定义监控
        """
        self.userMetrics = userMetrics

    def setAddonsConfig(self, addonsConfig):
        """
        :param addonsConfig: (Optional) 集群组件配置
        """
        self.addonsConfig = addonsConfig

