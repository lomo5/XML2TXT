# XML2TXT
xml文件处理，两个py文件分别是两种方法。
- Xml2Txt.py使用xml.sax处理xml文件。
- opAsTxt.py采用文本文件的方法处理xml。原因是xml.sax在tag有错（主要是前后不匹配）的情况下报错，无法忽略错误。
