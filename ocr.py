from paddleocr import PaddleOCR, draw_ocr
import os
import re
from PIL import Image
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os


def image_path(dirname):
    result = []
    file_list = os.listdir(dirname)  # 获取文件列表
    sorted_file_list = sorted(file_list,
                              key=custom_sort)  # 使用自定义排序函数对文件名列表进行排序
    for filename in sorted_file_list:
        path = os.path.join(dirname, filename)  # 构建文件路径
        value = prompt_value(path)  # 获取ocr提取的输入输出
        result.append({"image_path": path, "prompt": value})
    print(result)
    return result


def custom_sort(filename):
    # 使用正则表达式提取文件名中的数字部分
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        return filename


def prompt_value(filename):
    # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
    # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    ocr = PaddleOCR(
        use_angle_cls=True, lang="ch"
    )  # need to run only once to download and load model into memory
    # img_path = '/home/PJLAB/meijiawen/Documents/puyu/知乎-混元/混元10.png'
    print
    result = ocr.ocr(filename, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    result = result[0]
    # image = Image.open(img_path).convert('RGB')
    # boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # print(txts)

    # scores = [line[1][1] for line in result]
    # im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')
    txts_string = ''.join(txts)
    return txts_string


# 创建一个新的工作簿
workbook = Workbook()
sheet = workbook.active

# 图片和对应的列表
image_list = image_path('/home/PJLAB/meijiawen/Documents/puyu/test')
# 在Excel中添加图片和列表
for index, item in enumerate(image_list, start=1):
    image_path = item["image_path"]
    list_data = item["prompt"]

    # 添加图片
    img = Image(image_path)
    img.width = 100  # 设置图片宽度
    img.height = 100  # 设置图片高度
    sheet.height = 20
    sheet.column_dimensions['A'].width = 15
    sheet.column_dimensions['B'].width = 80

    sheet.add_image(img, f'A{index}')  # 将图片添加到指定单元格

    # 添加列表

    sheet.cell(row=index, column=2, value=list_data)

# 保存Excel文件
workbook.save("output.xlsx")