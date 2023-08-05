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


class WebWhiteListRuleSpec(object):

    def __init__(self, name, mode, value, action, status, key=None, pattern=None):
        """
        :param name:  白名单规则名称
        :param mode:  模式:<br>- 0: uri<br>- 1: ip<br>- 2: cookie<br>- 3: geo<br>- 4: header
        :param key: (Optional) 匹配 key, mode 为 cookie 和 header 时必传. <br>- mode 为 cookie 时, 传 cookie 的 name<br>- mode 为 header 时, 传 header 的 key
        :param value:  匹配 value. <br>- mode 为 uri 时, 传要匹配的 uri<br>- mode 为 ip 时, 传引用的 ip 黑白名单 Id<br>- mode 为 cookie 时, 传 cookie 的 value<br>- mode 为 geo 时, 传 geo 区域编码以 ',' 分隔的字符串. 查询 <a href='http://docs.jdcloud.com/anti-ddos-pro/api/describewebrulewhitelistgeoareas'>describeWebRuleWhiteListGeoAreas</a> 接口获取可设置的地域编码列表<br>- mode 为 header 时, 传 header 的 value
        :param pattern: (Optional) 匹配规则, mode 为 uri, cookie 和 header 时必传. 支持以下匹配规则: <br>- 0: 完全匹配<br>- 1: 前缀匹配<br>- 2: 包含<br>- 3: 正则匹配<br>- 4: 后缀匹配
        :param action:  命中后处理动作. <br>- 0: 放行<br>- 1: CC 防护
        :param status:  规则状态. <br>- 0: 关闭<br>- 1: 开启
        """

        self.name = name
        self.mode = mode
        self.key = key
        self.value = value
        self.pattern = pattern
        self.action = action
        self.status = status
