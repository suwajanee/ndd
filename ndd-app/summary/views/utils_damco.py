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

    # Alignment
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

    # Background color
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
