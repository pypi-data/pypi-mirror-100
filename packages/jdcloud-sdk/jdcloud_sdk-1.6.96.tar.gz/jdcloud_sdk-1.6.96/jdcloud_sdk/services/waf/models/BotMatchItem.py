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


class BotMatchItem(object):

    def __init__(self, field, logic, value, ):
        """
        :param field:  匹配字段，ruleType为general时，可为ip,uri,user_agent,referer,cookie， uri只能设置一个。ruleType为advanced时，可为fingerExist(是否存在),fingerValid(合法性)
        :param logic:  0-完全匹配 1-包含匹配, field为fingerExist/fingerValid时无意义。
        :param value:  filed为ip时支持8/16/24位掩码和完全匹配，field为uri且logic为0时需以"/"开头
        """

        self.field = field
        self.logic = logic
        self.value = value
