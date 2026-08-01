import pdfplumber as plumber

with plumber.open("./data/raw/bns.pdf") as pdf:
	for i in range(1):
		page = pdf.pages[16-1]
		height = page.height
		width = page.width
		cropped = page.crop((0,0,width,height - 65)) #left,up,right,down
		for i in cropped.extract_text_lines():
			print(i["text"])
		# print(cropped.extract_text_lines()[1]['text'])