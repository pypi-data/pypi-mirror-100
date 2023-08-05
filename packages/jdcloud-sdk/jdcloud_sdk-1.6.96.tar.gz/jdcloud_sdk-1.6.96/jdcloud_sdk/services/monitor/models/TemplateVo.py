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


class TemplateVo(object):

    def __init__(self, createTime=None, description=None, pin=None, rulesCount=None, serviceCode=None, templateId=None, templateName=None, templateRules=None, templateRulesString=None, templateType=None, updateTime=None):
        """
        :param createTime: (Optional) 
        :param description: (Optional) 模板描述
        :param pin: (Optional) 用户
        :param rulesCount: (Optional) 模板内包含的规则数量
        :param serviceCode: (Optional) 模板所属资源类型
        :param templateId: (Optional) 模板id
        :param templateName: (Optional) 模板名称
        :param templateRules: (Optional) 模板内包含的规则
        :param templateRulesString: (Optional) 模板内包含的提供给前端的拼接好的规则
        :param templateType: (Optional) 模板类型，区分默认模板和用户自定义模板：1表示默认模板，2表示用户自定义模板
        :param updateTime: (Optional) 
        """

        self.createTime = createTime
        self.description = description
        self.pin = pin
        self.rulesCount = rulesCount
        self.serviceCode = serviceCode
        self.templateId = templateId
        self.templateName = templateName
        self.templateRules = templateRules
        self.templateRulesString = templateRulesString
        self.templateType = templateType
        self.updateTime = updateTime
