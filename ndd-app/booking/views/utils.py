import xlwt

class StyleXls():
    def header_style(self):
        style = xlwt.XFStyle()

        # font
        font = xlwt.Font()
        font.bold = True
        style.font = font

        # borders
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THICK
        borders.right = xlwt.Borders.THICK
        borders.left = xlwt.Borders.THICK
        borders.bottom = xlwt.Borders.THICK
        style.borders = borders

        # pattern
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        style.pattern = pattern

        # alignment
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        style.alignment = alignment

        return style

    def bg_black(self):
        style = xlwt.XFStyle()
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['black']
        style.pattern = pattern
        return style

    def border_cell(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def cancel_row(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
        return pattern

    def bg_aqua(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['aqua']
        return pattern

    def bg_light_orange(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['light_orange']
        return pattern

    def bright_green(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['bright_green']
        return pattern

    def align_left(self):
        alignment = xlwt.Alignment()
        alignment.horz = 1
        return alignment
