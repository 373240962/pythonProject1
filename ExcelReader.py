from time import strftime

import xlrd
import xlsxwriter
from xlrd import xldate_as_tuple, xldate_as_datetime
import pandas as pd
import os
import shutil

def readExcel(fileName):
    data = xlrd.open_workbook(fileName)

    for i in range(0,2):
        table = data.sheets()[i]

    for rown in range(table.nrows):
        if rown > 1:
            json1 = {'city': '屏山', 'year': xldate_as_datetime(table.cell_value(rown, 0),0).year, 'date': xldate_as_datetime(table.cell_value(rown, 0), 0), 'Q': int(table.cell_value(rown, 1))}
            json2 = {'city': '寸滩', 'year': xldate_as_datetime(table.cell_value(rown, 3),0).year, 'date': xldate_as_datetime(table.cell_value(rown, 3), 0), 'Q': int(table.cell_value(rown, 4))}
            json3 = {'city': '宜昌', 'year': xldate_as_datetime(table.cell_value(rown, 6),0).year, 'date': xldate_as_datetime(table.cell_value(rown, 6), 0), 'Q': int(table.cell_value(rown, 7))}

            array1.append(json1)
            array2.append(json2)
            array3.append(json3)

    df1 = pd.DataFrame(array1)
    df2 = pd.DataFrame(array2)
    df3 = pd.DataFrame(array3)

    # list = df1.loc[df1.groupby(df1['year'])['Q'].idxmax()].apply(pd.Series.tolist).tolist()
    # list1 = df2.loc[df1.groupby(df1['year'])['Q'].idxmax()].apply(pd.Series.tolist).tolist()
    # list2 = df3.loc[df1.groupby(df1['year'])['Q'].idxmax()].apply(pd.Series.tolist).tolist()

    start = fileName.rindex('\\')
    newFileName = fileName[: start+1]
    wb = xlsxwriter.Workbook(newFileName + '皮神.xlsx')
    ws = wb.add_worksheet('皮神')
    ws.activate()
    title = ['city', 'year', 'date', 'Q']
    ws.write_row(0, 0, title)

    data = df1.loc[df1.groupby(df1['year'])['Q'].idxmax()].values
    for i in range(len(data)):
        data[i][2] = data[i][2].strftime('%Y年%m月%d日')
        ws.write_row(i, 0, data[i])

    data2 = df2.loc[df2.groupby(df2['year'])['Q'].idxmax()].values
    for i in range(len(data2)):
        data2[i][2] = data2[i][2].strftime('%Y年%m月%d日')
        ws.write_row(i + len(data), 0, data2[i])

    data3 = df3.loc[df3.groupby(df3['year'])['Q'].idxmax()].values
    for i in range(len(data3)):
        data3[i][2] = data3[i][2].strftime('%Y年%m月%d日')
        ws.write_row(i + len(data) + len(data2), 0, data3[i])

    wb.close()




def open_file(file_name):

    print(file_name)  # Press Ctrl+F8 to toggle the breakpoint.
    list = os.listdir(file_name)
    for file in list:
        fileN = os.path.join(file_name, file)
        print("当前目录:" + file_name)
        if os.path.isdir(fileN):
            print(fileN)
            open_file(fileN)
        else:
            (filepath, tempfilename) = os.path.split(fileN)
            print("路径:" + filepath)
            print("文件名:" + tempfilename)
            (shotname, extension) = os.path.splitext(tempfilename)
            print("shotname:" + shotname)
            print("extension:" + extension)
            if extension == ".xlsx" | extension == ".xls":
                print("源文件:" + fileN)
                readExcel(fileN)

if __name__ == '__main__':
    fileName = input("请输入文件夹：")
    open_file(fileName)
