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


class CreateAdminProductRequest(JDCloudRequest):
    """
    新建产品
    """

    def __init__(self, parameters, header=None, version="v2"):
        super(CreateAdminProductRequest, self).__init__(
            '/regions/{regionId}/loongrayinstances/{instanceId}/productsAdmin', 'POST', header, version)
        self.parameters = parameters


class CreateAdminProductParameters(object):

    def __init__(self, regionId, instanceId, productName, productType, collDeviceType):
        """
        :param regionId: 地域ID
        :param instanceId: IoT Engine实例ID信息
        :param productName: 产品名称，名称不可为空，3-30个字符，只支持汉字、英文字母、数字、下划线“_”及中划线“-”，必须以汉字、英文字母及数字开头结尾
        :param productType: 节点类型，取值：
0：设备。设备不能挂载子设备。可以直连物联网平台，也可以作为网关的子设备连接物联网平台
1：网关。网关可以挂载子设备，具有子设备管理模块，维持子设备的拓扑关系，和将拓扑关系同步到物联网平台

        :param collDeviceType: 产品名下所有设备的采集器类型
        """

        self.regionId = regionId
        self.instanceId = instanceId
        self.productName = productName
        self.productType = productType
        self.productDescription = None
        self.templateId = None
        self.internalTags = None
        self.collDeviceType = collDeviceType

    def setProductDescription(self, productDescription):
        """
        :param productDescription: (Optional) 产品描述，80字符以内
        """
        self.productDescription = productDescription

    def setTemplateId(self, templateId):
        """
        :param templateId: (Optional) 物模型模板ID，内部参数，用户不可见，默认为自定义
        """
        self.templateId = templateId

    def setInternalTags(self, internalTags):
        """
        :param internalTags: (Optional) 内部标签，内部参数，用户不可见，隐藏标签：hidden:true
        """
        self.internalTags = internalTags

