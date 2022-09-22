# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import shutil


def open_file(file_name):
    # Use a breakpoint in the code line below to debug your script.

    new_file_name = file_name + "\test"
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
            if extension == ".JPG":
                print("源文件:" + fileN)
                print("目标目录:" + new_file_name + "\\" + tempfilename)
                shutil.move(fileN, new_file_name + "\\" + tempfilename)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_name = input("请输入文件夹：")
    open_file(file_name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
