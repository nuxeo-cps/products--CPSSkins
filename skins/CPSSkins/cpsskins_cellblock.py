##parameters=**options
# $Id$
"""
This script produces the rendering of a cell block, that is a block of cells.
A block of cells contains columns, containing in turn an optional cell sizer
and cells.
"""

shield = options.get('shield', True)
enable_esi = options.get('enable_esi')
boxedit = options.get('boxedit')
template = options.get('template')
context_obj = options['context_obj']
maxcols = context['maxcols']
# This variable is to know if we should hide this cell block if all
# contained cells haven't any content. There is a choice here because
# sometimes it might be interesting to have empty cells when those
# empty cells are used to have a background image or for layout purpose.
hidden_empty = context.getProperty('hidden_empty')

render = ''
empty = True
objects = context.getObjects()
# columns is a list of cells
columns = []

for x_pos in range(int(maxcols)):
    # cells is a list of tuples describing a cell sizer and a list
    # of cells.
    cells = []
    objects_in_xpos = objects.get(x_pos)
    cell_sizer = objects_in_xpos.get('cellsizer')
    column_width = cell_sizer and 'style="width: %s"' % cell_sizer.cellwidth or ''
    contents_in_xpos = objects_in_xpos['contents']
    for content in contents_in_xpos:
        render_cell = content.render_cache(shield=shield,
                                           context_obj=context_obj,
                                           enable_esi=enable_esi,
                                           boxedit=boxedit, template=template)
        cell_style_position = ('style="text-align:%s;padding:%s"'
                               % (content.align, content.margin))
        style_def = content.getCSSLayoutStyle()
        cell_style = style_def and 'style="%s"' % style_def or ''
        class_def = content.getCSSClass(level=2)
        cell_class = class_def and 'class="%s"' % class_def or ''
        cell = (cell_style_position, cell_style, cell_class, render_cell)
        if render_cell.strip() != '' or not hidden_empty:
            if empty:
                empty = False
            cells.append(cell)
    if cells:
        columns.append((column_width, cells))

if empty:
    return render

CELL_CONTENT_TEMPLATE = r"""<div %(style_position)s>
  <div %(class)s %(style)s>
    %(cell)s
  </div>
</div>
"""
# " <- Needed for Emacs Python mode, argh

COLUMN_TEMPLATE = r"""<td valign="top" %(style)s>
  %(cells)s
</td>
"""
# " <- Needed for Emacs Python mode, argh

CELL_BLOCK_TEMPLATE = r"""<table summary="%(summary)s" width="100%%"
cellpadding="0" cellspacing="0" %(class)s %(style)s>
  <tr>
    %(cells)s
  </tr>
</table>
"""
# " <- Needed for Emacs Python mode, argh

render_columns = ''
for column in columns:
    column_width = column[0]
    column_cells = column[1]
    render_styled_cells = ''
    for cell in column_cells:
        cell_style_position = cell[0]
        cell_style = cell[1]
        cell_class = cell[2]
        render_cell = cell[3]
        render_styled_cells += CELL_CONTENT_TEMPLATE % {
            'class': cell_class,
            'style_position': cell_style_position,
            'style': cell_style,
            'cell': render_cell,
            }

    render_columns += COLUMN_TEMPLATE % {
        'cells': render_styled_cells,
        'style': column_width,
        }

style_def = context.getCSSLayoutStyle()
cell_block_style = style_def and 'style="%s"' % style_def or ''
class_def = context.getCSSClass(level=2)
cell_block_class = class_def and 'class="%s"' % class_def or ''
render = CELL_BLOCK_TEMPLATE % {
    'summary': context['title'],
    'class': cell_block_class,
    'style': cell_block_style,
    'cells': render_columns,
    }

return render
