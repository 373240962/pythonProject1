class ReadResult:
    '所有统计结果的基类'
    empCount = 0

    def __init__(self, fileName, keyWord, count):
        self.fileName = fileName
        self.keyWord = keyWord
        self.count = count
        ReadResult.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % ReadResult.empCount)

    def displayMe(self):
        print("文件名 : ", self.fileName, ", 关键字: ", self.keyWord, ", 出现次数: ", self.count)