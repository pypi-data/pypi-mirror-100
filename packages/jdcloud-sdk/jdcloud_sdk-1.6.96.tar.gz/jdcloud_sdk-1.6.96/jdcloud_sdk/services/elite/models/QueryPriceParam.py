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


class QueryPriceParam(object):

    def __init__(self, cmd, packageCount, orderList, ):
        """
        :param cmd:  操作类型 1:创建 2:续费 3:升降配
        :param packageCount:  打包购买包数
        :param orderList:  
        """

        self.cmd = cmd
        self.packageCount = packageCount
        self.orderList = orderList
