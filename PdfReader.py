import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import xlsxwriter
import os

from ReadResult import ReadResult

keyWordList = ['社会责任', '社会', '责任']

pool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='read_pdf_')

# logging.propagate = False
# logging.getLogger().setLevel(logging.ERROR)

dataformat = '%Y-%m-%d %H:%M:%S'

def open_file(file_name):
    # Use a breakpoint in the code line below to debug your script.

    listResult = []

    print(file_name)  # Press Ctrl+F8 to toggle the breakpoint.
    list = os.listdir(file_name)
    for file in list:
        fileN = os.path.join(file_name, file)
        print("当前目录:" + file_name)
        if os.path.isdir(fileN):
            print(fileN)
            listResult.extend(open_file(fileN))
        else:
            (filepath, tempfilename) = os.path.split(fileN)
            print("路径:" + filepath)
            print("文件名:" + tempfilename)
            (shotname, extension) = os.path.splitext(tempfilename)
            print("shotname:" + shotname)
            print("extension:" + extension)
            if extension == ".pdf" or extension == ".PDF":
                print("源文件:" + fileN)
                listResult.append(pool.submit(readPdf, fileN, shotname, tempfilename))

    return listResult


def readPdf(file_path, shotname, tempfilename):
    print(datetime.datetime.now().strftime(dataformat) + ': 开始读取pdf文件:-------' + shotname + '\n')
    listResult = []
    with open(file_path, 'rb') as file:
        resource_manager = PDFResourceManager()
        return_str = StringIO()
        lap_params = LAParams()
        device = TextConverter(resource_manager, return_str, laparams=lap_params)
        process_pdf(resource_manager, device, file)
        device.close()
        content = return_str.getvalue()
        _content = content.replace('\n', '')
        createTxtFile(file_name, shotname, _content)
        print(datetime.datetime.now().strftime(dataformat) + ': 读取pdf文件结束:--------' + shotname + '\n')
        for key in keyWordList:
            print(datetime.datetime.now().strftime(dataformat) + ': ' + shotname + ':开始关键字搜索:-----------' + key + '\n')
            # 定义对象保存
            readResult = ReadResult(tempfilename, key, content.count(key))
            listResult.append(readResult)
            print(datetime.datetime.now().strftime(dataformat) + ': ' + shotname + ':关键字搜索结束,----------关键字:' + key + ',-----------出现次数:' + str(readResult.count) + '\n')
        return listResult


def createTxtFile(path, filename, content):
    with open(path + '\\' + filename + '.txt', 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    file_name = input("请输入文件夹：")
    tasks = []
    tasks.extend(open_file(file_name))
    wait(tasks, return_when=ALL_COMPLETED)
    listr = []
    for task in tasks:
        listr.extend(task.result())

    wb = xlsxwriter.Workbook(file_name + '\\关键字统计.xlsx')
    ws = wb.add_worksheet('按文件统计结果')
    ws.activate()
    title = ['文件名', '关键字', '出现次数']
    ws.write_row(0, 0, title)
    for i in range(len(listr)):
        rowData = [listr[i].fileName, listr[i].keyWord, listr[i].count]
        ws.write_row(i, 0, rowData)

    wb.close()

    # for re in listr:
    #     re.displayMe()
