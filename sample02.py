from reportlab.pdfgen.canvas import Canvas
from PollyReports import *
from testdata import data

rpt = Report(data)
rpt.detailband = Band([
    Element((36, 0), ("Helvetica", 11), key = "name"),
    Element((700, 0), ("Helvetica", 11), key = "amount", align = "right"),
])

canvas = Canvas("sample02.pdf", (72*21, 72*29))
rpt.generate(canvas)
canvas.save()
