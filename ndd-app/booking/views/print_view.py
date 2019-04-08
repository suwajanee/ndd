# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.six import BytesIO

import xhtml2pdf.pisa as pisa


def render_pdf(path, params):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Rendering PDF", status=400)
        