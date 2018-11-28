#!/usr/bin/python
# -*- coding: utf-8 -*-

import javalang  # 可以在https://github.com/c2nes/javalang得到
import sys
import os
import re
import random


# 获得文件路径
def GetPath():
    pathprefix = os.getcwd()
    if sys.platform == 'win32':
        pathsuffix = r'\assign1\src'
        pathjoin = '\\'
    else:
        pathsuffix = '/assign1/src'
        pathjoin = '/'
    return pathprefix + pathsuffix + pathjoin


# 筛选java文件
def IsSubString(SubStrList, Str):
    flag = True
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


# 美化格式
def PrintStar():
    print('*' * 20)


# 列出java文件
def ListFile(FindPath, FlagStr):
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                if (IsSubString(FlagStr, fn)):
                    FileList.append(fn)

            else:
                FileList.append(fn)

    if (len(FileList) > 0):
        FileList.sort()

    return FileList


# 选择类文件
def ChooseClass(FileNames):
    PrintStar()
    for idx, val in enumerate(FileNames, start=1):
        print(idx, val)
    PrintStar()


# 备份源文件
def Backupfile(Path, Origin):
    with open(Path + '.backup', 'w', encoding='utf-8') as f:
        f.write(Origin)
    return


# 选择方法
def ChooseMethod(ClassFile):
    tree = javalang.parse.parse(ClassFile)

    method = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        method.append(node.name)
    PrintStar()
    for idx, val in enumerate(method, start=1):
        print(idx, val, '()')
    PrintStar()
    return method


# 分割方法
def SplitMethod(ClassFile, MethodName):
    fixed = r'public.*'
    pattern = fixed + MethodName + r'\((.*?)\)'
    pos = re.search(pattern, ClassFile)
    input = ClassFile[pos.span()[0]:]
    # PrintStar()
    # print('split input', input)
    # PrintStar()
    i = input.find('{')
    stack = ['{']

    while len(stack) > 0:
        i += 1
        if input[i] == '}':
            if stack.pop() == '{':
                pass
            # else:
            #     stack.append('}')
            #     stack.append('}')
        elif input[i] == '{':
            stack.append('{')
        else:
            pass

    postion = [pos.span()[0], pos.span()[0] + i + 1]
    # print(postion)
    return postion


# 选择错误注入
def FaultInjection(Method):
    selectfault = ['完成注入', 'Return语句替换', '逻辑符号替换', '关系符替换', '常数替换', '运算符号替换']
    for idx, val in enumerate(selectfault):
        print(idx, val, )
    while 1:
        selnum3 = int(input("请选择需要的错误类型:"))
        if selnum3 == 1:
            tmp = ReturnFaultInjection(Method)
            if (tmp != -1):
                Method = tmp
                PrintStar()
                print(Method)
                PrintStar()
            else:
                print('没有Return语句，请重选')
        elif selnum3 == 2:
            tmp = LogicalFaultInjection(Method)
            if (tmp != -1):
                Method = tmp
                PrintStar()
                print(Method)
                PrintStar()
            else:
                print('没有逻辑判断语句，请重选')
        elif selnum3 == 3:
            tmp = RelationalFaultInjection(Method)
            if (tmp != -1):
                Method = tmp
                PrintStar()
                print(Method)
                PrintStar()
            else:
                print('没有关系判断语句，请重选')
        elif selnum3 == 4:
            Method = ConstantFaultInjection(Method)
            PrintStar()
            print(Method)
            PrintStar()
        elif selnum3 == 5:
            tmp = OperatorFaultInjection(Method)
            if (tmp != -1):
                Method = tmp
                PrintStar()
                print(Method)
                PrintStar()
            else:
                print('没有运算符号，请重选')
        else:
            break
    return Method


# Return错误注入
def ReturnFaultInjection(Method):
    if (Method.find('return false') != -1 or Method.find('return true') != -1):
        Method = Method.replace('return false', '###')
        Method = Method.replace('return true', '***')
    else:
        return -1

    Method = Method.replace('###', 'return true')
    Method = Method.replace('***', 'return false')

    return Method


def LogicalFaultInjection(Method):
    if (Method.find('&&') != -1 or Method.find('||') != -1):
        Method = Method.replace('&&', '###')
        Method = Method.replace('||', '***')
    else:
        return -1

    Method = Method.replace('###', '||')
    Method = Method.replace('***', '&&')

    return Method


def RelationalFaultInjection(Method):
    if (Method.find('>') != -1 or Method.find('>=') != -1 or Method.find('<') != -1 or Method.find(
            '<=') != -1 or Method.find('==') != -1 or Method.find('!=') != -1):
        Method = Method.replace('>', '###')
        Method = Method.replace('>=', '***')
        Method = Method.replace('<', '@@@')
        Method = Method.replace('<=', '$$$')
        Method = Method.replace('==', '%%%')
        Method = Method.replace('!=', '^^^')
    else:
        return -1

    Method = Method.replace('###', '>=')
    Method = Method.replace('***', '>')
    Method = Method.replace('@@@', '<=')
    Method = Method.replace('$$$', '<')
    Method = Method.replace('%%%', '!=')
    Method = Method.replace('^^^', '==')
    return Method


def ConstantFaultInjection(Method):
    tmp = ''
    for c in Method:
        c = re.sub(r'\d', str(random.randrange(10)), c)
        tmp += c
    Method = tmp
    return Method


def OperatorFaultInjection(Method):
    if (Method.find('%') != -1 or Method.find('-') != -1 or Method.find('*') != -1 or Method.find('/') != -1):
        Method = Method.replace('%', '###')
        Method = Method.replace('-', '%%%')
        Method = Method.replace(' * ', '@@@')
        Method = Method.replace(' / ', '$$$')
    # Method = Method.replace('==', '%%%')
    # Method = Method.replace('!=', '^^^')
    else:
        return -1

    Method = Method.replace('###', '/')
    Method = Method.replace('%%%', '+')
    Method = Method.replace('@@@', ' - ')
    Method = Method.replace('$$$', ' % ')
    # Method = Method.replace('%%%', '!=')
    # Method = Method.replace('^^^', '==')
    return Method


# 保存文件
def Writetofile(Path, Injected):
    with open(Path, 'w', encoding='utf-8') as f:
        f.write(Injected)
    return 1


# 比较文件变化
def CompareFile(Path1, Path2):
    PrintStar()
    with open(Path1, 'r', encoding='utf-8') as f1, open(Path2, 'r', encoding='utf-8') as f2:
        for line_no, (line1, line2) in enumerate(zip(f1, f2)):
            if line1 != line2:
                print('line ' + str(line_no) + '\t' + line1.strip() + ' change to ' + line2.strip())
    PrintStar()


if __name__ == '__main__':
    path = GetPath()
    file_name = ListFile(path, 'java')
    ChooseClass(file_name)
    selnum1 = int(input("请选择需要的类文件:"))
    path_abs = path + file_name[selnum1 - 1]
    with open(path_abs, 'r', encoding='utf-8') as f:
        classfile = f.read()
    Backupfile(path_abs, classfile)
    method = ChooseMethod(classfile)

    selnum2 = int(input("请选择需要的方法:"))
    methodpos = SplitMethod(classfile, method[selnum2 - 1]) #选择方法的位置

    methodtxt = classfile[methodpos[0]:methodpos[1]]
    PrintStar()
    print(methodtxt)
    PrintStar()

    methodtxt = FaultInjection(methodtxt)

    classfile = classfile[:methodpos[0]] + methodtxt + classfile[methodpos[1]:]
    if(input("需要展示注入后的代码吗？y/n:") == 'y'):
        PrintStar()
        print(classfile)
        PrintStar()

    if(Writetofile(path_abs, classfile) == 1):
        PrintStar()
        print('注入完成！')
        PrintStar()

    CompareFile(path_abs + '.backup', path_abs)
