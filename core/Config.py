#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
import yaml

f = open('config.yaml','r', encoding='UTF-8')
content = yaml.load(f)
print(content)