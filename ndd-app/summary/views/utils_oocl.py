import xlwt

class StyleXls():
    def font_name(self):
        font = xlwt.Font()
        font.name = 'BrowalliaUPC'
        return font

    # Title
    def title_style(self):
        style = xlwt.XFStyle()

        # font
        font = self.font_name()
        font.bold = True
        font.height = 20*13
        style.font = font

        # alignment
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        style.alignment = alignment

        return style

    # Header table
    def header_style(self):
        style = xlwt.XFStyle()

        # font
        font = self.font_name()
        font.height = 20*13
        style.font = font

        # borders
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.borders = borders

        # alignment
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        style.alignment = alignment

        return style

    # Border
    def border_cell(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_left(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        return borders

    def border_left_bottom(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_right(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        return borders

    def border_right_bottom(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_left_right(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        return borders

    def border_left_right_bottom(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    # Background color
    def bg_turquoise(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['turquoise']
        return pattern

    def bg_tan(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['tan']
        return pattern

    # Alignment
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

    def align_right(self):
        alignment = xlwt.Alignment()
        alignment.horz = 3
        alignment.vert = 1
        return alignment

    # Font
    def font_size_12(self):
        font = self.font_name()        
        font.height = 20*12
        return font

    def font_size_12_bold(self):
        font = self.font_name()        
        font.bold = True
        font.height = 20*12
        return font

    def font_size_13(self):
        font = self.font_name()
        font.height = 20*13
        return font

    def font_size_14(self):
        font = self.font_name()
        font.height = 20*14
        return font

    def font_size_14_bold(self):
        font = self.font_name()
        font.bold = True
        font.height = 20*14
        return font

    def font_size_16(self):
        font = self.font_name()
        font.height = 20*16
        return font

    def font_size_16_bold(self):
        font = self.font_name()
        font.bold = True
        font.height = 20*16
        return font

    def font_size_18(self):
        font = self.font_name()
        font.height = 20*18
        return font

    def font_size_18_bold(self):
        font = self.font_name()
        font.bold = True
        font.height = 20*18
        return font

    def font_bold(self):
        font = self.font_name()
        font.bold = True
        return font
