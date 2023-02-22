from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup

def html_to_pdf(html_file, pdf_file):
    soup = BeautifulSoup(open(html_file, "r"), 'html.parser')
    html = soup.prettify()

    c = canvas.Canvas(pdf_file)
    c.setPageSize((8.5*72, 11*72))

    c.drawString(72, 720, html)

    c.showPage()
    c.save()

html_to_pdf("Test.html", "output_file.pdf")
