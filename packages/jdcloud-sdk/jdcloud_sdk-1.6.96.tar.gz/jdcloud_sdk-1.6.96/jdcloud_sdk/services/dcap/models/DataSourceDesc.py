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


class DataSourceDesc(object):

    def __init__(self, dataSourceId=None, dataSourceType=None, dataSourceName=None, dataSourceAddr=None, dataSourcePort=None, dataSourceDbName=None, region=None, vpcId=None, subnetId=None, protectStatus=None, kmsKeyId=None, keyCipher=None, encryptAlgo=None, indexAlgo=None):
        """
        :param dataSourceId: (Optional) 数据源ID
        :param dataSourceType: (Optional) 数据源类型: 1->MySQL
        :param dataSourceName: (Optional) 数据源名称
        :param dataSourceAddr: (Optional) 数据源地址，域名或IP
        :param dataSourcePort: (Optional) 数据源端口
        :param dataSourceDbName: (Optional) 数据源数据库名称
        :param region: (Optional) 区域
        :param vpcId: (Optional) VPC ID
        :param subnetId: (Optional) Subnet ID
        :param protectStatus: (Optional) 防护状态: true->已防护,false->未防护
        :param kmsKeyId: (Optional) KMS 密钥ID
        :param keyCipher: (Optional) 数据密钥密文
        :param encryptAlgo: (Optional) 加密算法，AES256/SM4
        :param indexAlgo: (Optional) 索引算法，SHA256/SM3
        """

        self.dataSourceId = dataSourceId
        self.dataSourceType = dataSourceType
        self.dataSourceName = dataSourceName
        self.dataSourceAddr = dataSourceAddr
        self.dataSourcePort = dataSourcePort
        self.dataSourceDbName = dataSourceDbName
        self.region = region
        self.vpcId = vpcId
        self.subnetId = subnetId
        self.protectStatus = protectStatus
        self.kmsKeyId = kmsKeyId
        self.keyCipher = keyCipher
        self.encryptAlgo = encryptAlgo
        self.indexAlgo = indexAlgo
