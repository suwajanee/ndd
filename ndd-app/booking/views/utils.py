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
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
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

    def bg_booking(self, index):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        color = ['pink', 'rose', 'coral', 'light_orange', 'gold', 'light_yellow', 'light_green', 'light_turquoise', 'pale_blue', 'periwinkle']
        pattern.pattern_fore_colour = xlwt.Style.colour_map[color[index]]
        return pattern

    def bg_none(self):
        pattern = xlwt.Pattern()
        # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        # pattern.pattern_fore_colour = xlwt.Style.colour_map['']
        return pattern

    def bg_bright_green(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['bright_green']
        return pattern

    def bg_sky_blue(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['sky_blue']
        return pattern

    def bg_yellow(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
        return pattern

    def align_left(self):
        alignment = xlwt.Alignment()
        alignment.horz = 1
        alignment.vert = 1
        return alignment

    def align_center(self):
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        return alignment

    def font_bold(self):
        font = xlwt.Font()
        font.bold = True
        return font
