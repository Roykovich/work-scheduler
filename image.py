from PIL import Image, ImageFont, ImageDraw
from collections import namedtuple


def position_tuple(*args):
    Position = namedtuple('Position', ['top', 'right', 'bottom', 'left'])
    if len(args) == 0:
        print('im happening')
        return Position(0, 0, 0, 0)
    elif len(args) == 1:
        return Position(args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return Position(args[0], args[1], args[0], args[1])
    elif len(args) == 3:
        return Position(args[0], args[1], args[2], args[1])
    else:
        return Position(args[0], args[1], args[2], args[3])

# How it was before my change (note the missing font argument)
# def draw_table(table, header=[], font={}, cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False):
def draw_table(table, header=[], cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False):
    """
    Draw a table using only Pillow
    table:    an 2d list, must be str
    header:   turple or list, must be str
    font:     an ImageFont object
    cell_pad: padding for cell, (top_bottom, left_right)
    margin:   margin for table, css-like shorthand
    align:    None or list, 'l'/'c'/'r' for left/center/right, length must be the max count of columns
    colors:   dict, as follows
    stock:    bool, set red/green font color for cells start with +/-
    """
    _color = {
        'bg': '#2c2f33',
        'cell_bg': '#2c2f33',
        'header_bg': '#23272a',
        'font': '#ffffff',
        'rowline': '#99aab5',
        'colline': '#99aab5',
        'red': 'red',
        'green': 'green',
    }
    _color.update(colors)

    _font = ImageFont.truetype("fira_code.ttf", 25)

    _margin = position_tuple(*margin)

    table = table.copy()
    if header:
        table.insert(0, header)
    row_max_hei = [0] * len(table)
    col_max_wid = [0] * len(max(table, key=len))
    for i in range(len(table)):
        for j in range(len(table[i])):
            col_max_wid[j] = max(_font.getsize(table[i][j])[0], col_max_wid[j])
            row_max_hei[i] = max(_font.getsize(table[i][j])[1], row_max_hei[i])
    tab_width = sum(col_max_wid) + len(col_max_wid) * 2 * cell_pad[0]
    tab_heigh = sum(row_max_hei) + len(row_max_hei) * 2 * cell_pad[1]

    tab = Image.new('RGBA', (tab_width + _margin.left + _margin.right, tab_heigh + _margin.top + _margin.bottom), _color['bg'])
    draw = ImageDraw.Draw(tab)

    draw.rectangle([(_margin.left, _margin.top), (_margin.left + tab_width, _margin.top + tab_heigh)], 
                   fill=_color['cell_bg'], width=0)
    if header:
        draw.rectangle([(_margin.left, _margin.top), (_margin.left + tab_width, _margin.top + row_max_hei[0] + cell_pad[1] * 2)], 
                       fill=_color['header_bg'], width=0)

    top = _margin.top
    for row_h in row_max_hei:
        draw.line([(_margin.left, top), (tab_width + _margin.left, top)], fill=_color['rowline'])
        top += row_h + cell_pad[1] * 2
    draw.line([(_margin.left, top), (tab_width + _margin.left, top)], fill=_color['rowline'])

    left = _margin.left
    for col_w in col_max_wid:
        draw.line([(left, _margin.top), (left, tab_heigh +_margin.top)], fill=_color['colline'])
        left += col_w + cell_pad[0] * 2
    draw.line([(left, _margin.top), (left, tab_heigh + _margin.top)], fill=_color['colline'])

    top, left = _margin.top + cell_pad[1], 0
    for i in range(len(table)):
        left = _margin.left + cell_pad[0]
        for j in range(len(table[i])):
            color = _color['font']
            if stock:
                if table[i][j].startswith('+'):
                    color = _color['red']
                elif table[i][j].startswith('-'):
                    color = _color['green']
            _left = left
            if (align and align[j] == 'c') or (header and i == 0):
                _left += (col_max_wid[j] - _font.getsize(table[i][j])[0]) // 2
            elif align and align[j] == 'r':
                _left += col_max_wid[j] - _font.getsize(table[i][j])[0]
            draw.text((_left, top), table[i][j], font=_font, fill=color)
            left += col_max_wid[j] + cell_pad[0] * 2
        top += row_max_hei[i] + cell_pad[1] * 2
    
    tab.save("horario.png")

    return tab
