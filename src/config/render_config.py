import config.config_loader as cfl


def get_max_sample():
    '''
    渲染的采样率
    '''
    key = 'max_sample'
    return int(cfl.get_item(key))


def get_output_height():
    '''
    渲染结果高度, 像素
    '''
    key = 'output_height'
    return int(cfl.get_item(key))


def get_output_width():
    '''
    渲染结果宽度, 像素
    '''
    key = 'output_width'
    return int(cfl.get_item(key))


def get_output_format():
    '''
    输出的格式
    '''
    key = 'output_format'
    return str.upper(cfl.get_item(key)) 


def get_render_count():
    '''
    一个批次输出多少图片
    '''
    key = 'render_count'
    return int(cfl.get_item(key))


def get_render_engine():
    '''
    选择渲染器
    '''
    key = 'render_engine'
    return str.upper(cfl.get_item(key))

