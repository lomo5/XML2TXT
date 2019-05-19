import os
import re
# 本程序以文本文件的形式处理xml文件（由于xml文件的tag有些错的，前后不对应，比如：<annotation>...</annoatation>（单词拼写错误））
# xml文件例子：
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
# 思路：
#   1、遍历当前文件夹下所有的子文件夹找到所有xml文件
#   2、取出含有<name>标签的行
#   3、由于文件中不止一个<name>标签，因此之后再判断<name>标签之间的文本用"_"切割是否可以分成两部分，从而取得例子中的<name>标签的内容
#   4、将文件名、严重程度、器官名称 写入index.txt文件
#


def read_xml_file(xmlfilename):
    # 读指定的xml文件，返回一个数组：[xml文件完整路径,严重程度,器官]
    txt = []
    xmlfile = open(xmlfilename, 'r')
    for line in xmlfile:
        startnum = line.find('<name>', 0, len(line))
        endnum = line.find('</name>', 0, len(line))
        if startnum != -1 and endnum != -1:
            content = line[startnum + 6:endnum]
            str1 = re.split(r'_', content)
            if len(str1) > 1:
                txt.append(xmlfilename+' '*(30-len(xmlfilename)))
                txt.append(str1[0][0:6]+'     ')
                txt.append(str1[1])
    xmlfile.close()
    return txt


if __name__ == '__main__':
    allfiles = []
    txtlines = []
    newtxt = open('./index.txt', 'a')
    # 遍历当前文件夹
    for root, dirs, files in os.walk("./"):
        # for di in dirs:
        #     print(os.path.join(root, di))
        for file in files:
            filename = os.path.join(root, file)
            if re.search(r'\.[xX][Mm][Ll]', filename):
                newline=read_xml_file(filename)
                newline.append('\n')
                if len(newline)==4:
                    txtlines.append(read_xml_file(filename))

                    newtxt.writelines(newline)

    newtxt.close()