# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

import json

inp_strr = '{"k1":123, "k2": "456", "k3:":"ares"}'
# 根据字符串书写格式，将字符串自动转换成 字典类型
inp_dict = json.loads(inp_strr)
print (inp_dict)

# 将python对象test转换json对象
test = [{"username":"测试","age":16},(2,3),1]
print(type(test))
python_to_json = json.dumps(test, ensure_ascii=False)
print(python_to_json)
print(type(python_to_json))

# 将json对象转换成python对象
json_to_python = json.loads(python_to_json)
print(json_to_python)
print(type(json_to_python))