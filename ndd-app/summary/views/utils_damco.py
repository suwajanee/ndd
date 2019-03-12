import xlwt

class StyleXls():
    def font_tahoma(self):
        font = xlwt.Font()
        font.name = 'Tahoma'
        return font

    # Font
    def font_size_16(self):
        font = self.font_tahoma()
        font.height = 20*16
        return font

    def font_size_16_bold(self):
        font = self.font_tahoma()
        font.bold = True
        font.height = 20*16
        return font

    def font_size_20_i(self):
        font = self.font_tahoma()
        font.italic = True
        font.height = 20*20
        return font

    def font_size_20_bold(self):
        font = self.font_tahoma()
        font.bold = True
        font.height = 20*20
        return font

    def font_size_30(self):
        font = self.font_tahoma()
        font.height = 20*30
        return font

    def font_size_28(self):
        font = self.font_tahoma()
        font.height = 20*28
        return font

    def font_size_26(self):
        font = self.font_tahoma()
        font.height = 20*26
        return font

    def font_size_26_bold(self):
        font = self.font_tahoma()
        font.bold = True
        font.height = 20*26
        return font

    def font_size_25(self):
        font = self.font_tahoma()
        font.height = 20*25
        return font

    def font_size_30_bold(self):
        font = self.font_tahoma()
        font.bold = True
        font.height = 20*30
        return font

    # Align
    def align_center_mid(self):
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        return alignment

    def align_center(self):
        alignment = xlwt.Alignment()
        alignment.horz = 2
        return alignment

    def align_left(self):
        alignment = xlwt.Alignment()
        alignment.horz = 1
        return alignment

    def align_right_mid(self):
        alignment = xlwt.Alignment()
        alignment.horz = 3
        alignment.vert = 1
        return alignment

    def align_right(self):
        alignment = xlwt.Alignment()
        alignment.horz = 3
        return alignment

    # Border
    def border_all(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_bottom(self):
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_left(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        return borders

    def border_right(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        return borders

    def border_left_bottom(self):
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_right_bottom(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_x_top(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        return borders

    def border_x_bottom(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    def border_x(self):
        borders = xlwt.Borders()
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        return borders

    def border_y(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    # Background
    def bg_light_green(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['light_green']
        return pattern

    def bg_light_gray(self):
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray50']
        return pattern


    # def title_style(self):
    #     style = xlwt.XFStyle()

    #     # font
    #     font = xlwt.Font()
    #     font.bold = True
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*13
    #     style.font = font

    #     # alignment
    #     alignment = xlwt.Alignment()
    #     alignment.horz = 2
    #     alignment.vert = 1
    #     style.alignment = alignment

    #     return style

    # def header_style(self):
    #     style = xlwt.XFStyle()

    #     # font
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*13
    #     style.font = font

    #     # borders
    #     borders = xlwt.Borders()
    #     borders.top = xlwt.Borders.THIN
    #     borders.right = xlwt.Borders.THIN
    #     borders.left = xlwt.Borders.THIN
    #     borders.bottom = xlwt.Borders.THIN
    #     style.borders = borders

    #     # alignment
    #     alignment = xlwt.Alignment()
    #     alignment.horz = 2
    #     alignment.vert = 1
    #     style.alignment = alignment

    #     return style

    # # def bg_black(self):
    # #     style = xlwt.XFStyle()
    # #     pattern = xlwt.Pattern()
    # #     pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # #     pattern.pattern_fore_colour = xlwt.Style.colour_map['black']
    # #     style.pattern = pattern
    # #     return style

    # def border_cell(self):
    #     borders = xlwt.Borders()
    #     borders.top = xlwt.Borders.THIN
    #     borders.right = xlwt.Borders.THIN
    #     borders.left = xlwt.Borders.THIN
    #     borders.bottom = xlwt.Borders.THIN
    #     return borders

    # def border_left(self):
    #     borders = xlwt.Borders()
    #     borders.left = xlwt.Borders.THIN
    #     return borders

    # def border_left_bottom(self):
    #     borders = xlwt.Borders()
    #     borders.left = xlwt.Borders.THIN
    #     borders.bottom = xlwt.Borders.THIN
    #     return borders

    # def border_right(self):
    #     borders = xlwt.Borders()
    #     borders.right = xlwt.Borders.THIN
    #     return borders

    # def border_right_bottom(self):
    #     borders = xlwt.Borders()
    #     borders.right = xlwt.Borders.THIN
    #     borders.bottom = xlwt.Borders.THIN
    #     return borders

    # def border_left_right(self):
    #     borders = xlwt.Borders()
    #     borders.left = xlwt.Borders.THIN
    #     borders.right = xlwt.Borders.THIN
    #     return borders

    # def border_left_right_bottom(self):
    #     borders = xlwt.Borders()
    #     borders.left = xlwt.Borders.THIN
    #     borders.right = xlwt.Borders.THIN
    #     borders.bottom = xlwt.Borders.THIN
    #     return borders

    # def bg_turquoise(self):
    #     pattern = xlwt.Pattern()
    #     pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #     pattern.pattern_fore_colour = xlwt.Style.colour_map['turquoise']
    #     return pattern

    # def bg_tan(self):
    #     pattern = xlwt.Pattern()
    #     pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    #     pattern.pattern_fore_colour = xlwt.Style.colour_map['tan']
    #     return pattern

    # def align_left(self):
    #     alignment = xlwt.Alignment()
    #     alignment.horz = 1
    #     alignment.vert = 1
    #     return alignment

    # def align_center(self):
    #     alignment = xlwt.Alignment()
    #     alignment.horz = 2
    #     alignment.vert = 1
    #     return alignment

    # def align_right(self):
    #     alignment = xlwt.Alignment()
    #     alignment.horz = 3
    #     alignment.vert = 1
    #     return alignment

    # def font_size_12(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*12
    #     return font

    # def font_size_12_bold(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.bold = True
    #     font.height = 20*12
    #     return font

    # def font_size_13(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*13
    #     return font

    # def font_size_14(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*14
    #     return font

    # def font_size_14_bold(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.bold = True
    #     font.height = 20*14
    #     return font

    # def font_size_16(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*16
    #     return font

    # def font_size_16_bold(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.bold = True
    #     font.height = 20*16
    #     return font

    # def font_size_18(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.height = 20*18
    #     return font

    # def font_size_18_bold(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.bold = True
    #     font.height = 20*18
    #     return font

    # def font_bold(self):
    #     font = xlwt.Font()
    #     font.name = 'BrowalliaUPC'
    #     font.bold = True
    #     return font
