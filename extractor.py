import pdfplumber as plumber
import re

def chunk_text(full_text):
	section_pattern = re.compile(r'^(\d+)\.\s+[A-Z]')

	lines = []
	chunks = {}
	chunk = []

	for idx in range(len(full_text)):
			lines.append(full_text[idx]['text'])

	i = 0
	while i != len(lines):
		if section_pattern.match(lines[i]):
			if not chunk:
				chunk.append(lines[i])
				i+=1
			else:
				chunks[chunk[0][0:2]] = chunk
				chunk = []
				chunk.append(lines[i])
				i+=1
		else:
			chunk.append(lines[i])
			i+=1
	print(chunks)

with plumber.open("./data/raw/bns.pdf") as pdf:
	for i in range(1):
		page = pdf.pages[27-1]
		height = page.height
		width = page.width
		cropped = page.crop((0,0,width,height - 65)) #left,up,right,down

		full_text = cropped.extract_text_lines()
		# lines = []

		# for idx in range(len(full_text)):
		# 	lines.append(full_text[idx]['text'])
		# section_pattern = re.compile(r'^(\d+)\.\s+[A-Z]')
		# for line in lines:
		# 	if section_pattern.match(line):
		# 				print(line[0:2])
		# print("##########################################")
		chunk_text(full_text)
