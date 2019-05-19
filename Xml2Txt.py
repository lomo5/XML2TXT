import os
import re
import xml.sax


# 使用sax包处理xml文件
# 扫描当前文件夹中的所有子文件夹，逐个处理其中的xml文件
# 找到xml文件中的<object>元素
# 例子：
#   <object>
# 		<name>SlightPalsy_Eyes</name>
# 		<pose>Left</pose>
# 		<bndbox>
# 			<xmin>1</xmin>
# 			<ymin>1</ymin>
# 			<xmax>159</xmax>
# 			<ymax>92</ymax>
# 		</bndbox>
# 	</object>
# 将其中<name>元素中的值取出，并识别和提取其中的单词（本例中为Slight和Eyes）
# 将取出的两个单词和当前xml文件的文件名一起写入当前文件夹的一个txt文件中
# ********本方法由于xml文件的tag有些错的，前后不对应，比如：<annotation>...</annoatation>（单词拼写错误），因此放弃！！！！！


class XmlHandler(xml.sax.ContentHandler):
    # 用来处理sax的处理xml元素的时间的handler类
    def __init__(self, filename):
        self.xmlFileName = filename
        self.toFindElement = 'name'
        self.serious = ['Strong', 'Slight', 'Normal']  # 严重程度
        self.organ = ['Eyes', 'Mouth']  # 部位
        self.currentTag = ''  # 当前读取的xml文件中的tag，用来在startElement函数和character函数之间共享当前tag
        self.currentContent = ''  # 当前标签的内容
        self.txt = []

    def startElement(self, tag, attributes):
        self.currentTag = tag

    def characters(self, content):
        if self.currentTag == 'name':
            self.currentContent = content
            # print('文件名:', self.xmlFileName, '; name标签内容:', self.currentContent)

    def endElement(self, tag):
        pass
        content = self.currentContent
        if self.currentTag == 'name':
            str1 = re.split(r'_', content)
            if len(str1) > 1:
                self.txt.append(self.xmlFileName)
                self.txt.append(str1[0][0:6])
                self.txt.append(str1[1])
        self.currentContent = ''
        self.currentTag = ''


def read_xml_file(xmlfilename):
    # 读指定的xml文件，返回一个数组：[xml文件完整路径,严重程度,器官]
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namespaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = XmlHandler(xmlfilename)
    parser.setContentHandler(Handler)

    parser.parse(xmlfilename)
    print('最终输出:', Handler.txt)
    return Handler.txt


if __name__ == '__main__':
    allfiles = []
    txtlines = []
    # 遍历当前文件夹
    for root, dirs, files in os.walk("./"):
        # for di in dirs:
        #     print(os.path.join(root, di))
        for file in files:
            filename = os.path.join(root, file)
            if re.search(r'\.[xX][Mm][Ll]', filename):
                txtlines.append(read_xml_file(filename))

    print(txtlines)
