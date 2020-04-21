#!env python
import sys
import  select
from enum import Enum

def IsEnglishChar(c):
    return 'a'<=c<='z' or 'A'<=c<='Z'

def isDigitChar(c):
    return '0'<=c<='9'

class CharType(Enum):
    OTHER_CHAR = 0,
    ENGLISH_CHAR = 1,
    CHINESE_CHAR =2,
    DIGIT_CHAR =3,
    BLANK_CHAR =4
    

def Count(lines):
    english_char = 0
    chinese_char = 0
    blank_char = 0
    digit_char = 0
    english_word = 0
    space_line = 0
    # 简单起见，12.32视为两个数字
    digit_word = 0
    for line in lines:
        if line=="\n" or line=="\r\n":
            space_line += 1
        t0 = CharType.OTHER_CHAR
        for i in range(len(line)):
            c = line[i]
            t1 = CharType.OTHER_CHAR
            if IsEnglishChar(c):
                t1 = CharType.ENGLISH_CHAR
                english_char += 1
            elif isDigitChar(c):
                t1 = CharType.DIGIT_CHAR
                digit_char += 1
            elif c==' ' or c=='\n' or c=='\t':
                t1 = CharType.BLANK_CHAR
                blank_char += 1
            elif '\u4e00' <= c <= '\u9fa5':
                t1 = CharType.CHINESE_CHAR
                chinese_char += 1
            if t0==CharType.ENGLISH_CHAR and t1!=CharType.ENGLISH_CHAR:
                english_word += 1
            elif t0==CharType.DIGIT_CHAR and t1!=CharType.DIGIT_CHAR:
                digit_word += 1
            t0 = t1
    print("English word :", english_word)
    print("Chinese char :", chinese_char)
    print("Digit word :", digit_word)
    print("Sum :", english_word+chinese_char+digit_word)
    print('-'*20)
    print('Blank char :', blank_char)
    print("Lines :", len(lines))
    print("Space line :", space_line)
    print("Non-space line :", len(lines)-space_line)


if __name__ == "__main__":
    argv = sys.argv
    # 判断stdin中是否有数据
    # select.select(rlist, wlist, xlist[, timeout])
    if select.select([sys.stdin,], [], [], 0.0)[0]:
        lines = sys.stdin.readlines()
        # print(sys.stdin.readlines())
        Count(lines)
    else:
        if len(argv)>1:
            filepath = argv[1]
            try:
                with open(filepath) as f:
                    lines = f.readlines()
                    Count(lines)
            except Exception:
                print(f"ERROR: Can't find file {argv[1]}",file=sys.stderr)




