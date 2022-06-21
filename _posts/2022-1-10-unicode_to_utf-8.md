---
layout: post
title:  "transfer from unicode to utf-8 encoding"
date:   2022-01-10 20:01:11 +0800
categories: encoding
---



Chinese character:      汉

its Unicode value:        U+6C49

convert 6C49 to binary:   01101100 01001001
                           1101100 01001001

```python
h= "汉"

# hex to binary, unicode value
h.encode("unicode_escape")
Out[112]: b'\\u6c49'  #hex decimal
int('6c49', 16)
Out[121]: 27721
bin(27721)
Out[120]: '0b110110001001001' #value of 6c49

# utf-8 value
h.encode("utf-8")
Out[113]: b'\xe6\xb1\x89'
bin(int('e6b189',16))
Out[129]: '0b111001101011000110001001'
```


format of UTF-8 byte sequences table:

| 1st Byte  |  2nd Byte |   3rd Byte |   4th Byte |   Number of Free Bits |  Maximum Expressible Unicode Value |
| --------- | --------- | ---------- | ---------- | --------------------- | ---------------------------------- |
| 0xxxxxxx  |    &nbsp; | &nbsp;     |  &nbsp;    |           7           |  007F hex (127)                    |  
| 110xxxxx  |  10xxxxxx | &nbsp;     |  &nbsp;    |      (5+6)=11         |  07FF hex (2047)                  |  
| 1110xxxx  |  10xxxxxx |   10xxxxxx |  &nbsp;    |     (4+6+6)=16        |  FFFF hex (65535)                |  
| 11110xxx  |  10xxxxxx |   10xxxxxx |   10xxxxxx |  (3+6+6+6)=21         |  10FFFF hex (1,114,111)           |

our Chinese character unicode is "6c49", 07FF<6c49<FFFF, so we should use third format to convert.

template:       1110xxxx    10xxxxxx    10xxxxxx
value of 6c49   01101100    01001001
result:         11100110    10110001    10001001



# ref
[difference between utf-8 and unicode](https://stackoverflow.com/questions/643694/what-is-the-difference-between-utf-8-and-unicode)

[utf-8](https://www.fileformat.info/info/unicode/utf8.htm)

