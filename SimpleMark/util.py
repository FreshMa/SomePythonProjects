def lines(file):
    '''
    列表生成式，产生每一行，并在最后一行添加换行
    '''
    for line in file: yield line
    yield '\n'

def blocks(file):
    '''
    对输入的文件进行分块，块是根据行与行之间有无空行来分割的，被空行独立出来的文字视为一个块
    '''
    block = []
    for line in lines(file):
        #如果line不为空，将其加到块block中
        if line.strip():
            block.append(line)
        #如果line为空，代表一个块已经结束，列表生成式生成的列表中添加一个新的块，并将临时变量block重置为空
        elif block:
            yield ''.join(block).strip()
            block = []
