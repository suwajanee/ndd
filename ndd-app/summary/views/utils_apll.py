import xlwt

class StyleXls():
    def font_std(self):
        font = xlwt.Font()
        font.name = 'AngsanaUPC'
        font.height = 20*16
        return font

    # Title
    def title_style(self):
        style = xlwt.XFStyle()

        # font
        font = self.font_std()
        font.bold = True
        font.height = 20*22
        font.colour_index = 4
        style.font = font

        return style

    # Header table
    def table_header_style(self):
        style = xlwt.XFStyle()

        # font
        font = self.font_std()
        font.height = 20*18
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

        # pattern
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        style.pattern = pattern

        return style

    # Background color
    def bg_turquoise(self):        
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['light_turquoise']
        return pattern

    def bg_rose(self):        
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['rose']
        return pattern

    def bg_gray(self): 
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        return pattern

    def bg_yellow(self): 
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
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

    # Border
    def border_all(self):
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        return borders

    # Cell Style
    def std_style(self, font, align):
        style = xlwt.XFStyle()

        if font:
            font = self.font_std()
            font.bold = True
            font.height = 20*18
            style.font = font

            style.pattern = self.bg_gray()
        else:
            style.font = self.font_std()

        if align == 0:
            style.alignment = self.align_left()
        elif align == 1:
            style.alignment = self.align_right()
            style.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        else:
            style.alignment = self.align_center()

        style.borders = self.border_all()

        return style

    def total_page(self, style_type):
        if style_type == 0:
            style = self.std_style(False, 2)
        elif style_type == 1:
            style = self.std_style(False, 1)
            style.pattern = self.bg_yellow()
        elif style_type == 2:
            style = self.std_style(True, 2)
            style.pattern = xlwt.Pattern()
        elif style_type == 3:
            style = self.std_style(True, 1)
            style.pattern = xlwt.Pattern()
        elif style_type == 4:
            style = self.std_style(True, 2)
            style.pattern = xlwt.Pattern()
            style.font.colour_index = 4

        style.borders = xlwt.Borders()

        return style

    def header_blue(self, font):
        style = xlwt.XFStyle()

        if font:
            font = self.font_std()
            font.bold = True
            font.height = 20*20
            style.font = font
        else:
            style.font = self.font_std()

        style.pattern = self.bg_turquoise()
        style.alignment = self.align_center()
        return style

    def header_rose(self, bg):
        style = xlwt.XFStyle()

        if bg:
            font = self.font_std()
            font.bold = True
            font.height = 20*20
            style.font = font

            style.pattern = self.bg_rose()
        else:
            font = self.font_std()

        style.alignment = self.align_center()
        return style


    


