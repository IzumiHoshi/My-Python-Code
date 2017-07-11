import re

str = r'\d{3}\-\d{3,8}'

str2 = r'\d{2}\-\d{3,8}'

str3 = '010-123)5'

str4 = '010 12345'

print(re.match(str, str3))

print(re.match(str2, str4))

ret = re.compile(r'^([\w\_]+)@([\w]+)(\.[a-z]+)+$')

m = ret.match('asdf123_000aa@qq.com.cn')

print(m)
print(m.group(0))
print(m.group(1))
print(m.group(2))