import pdfplumber as plumber
import re
from pprint import pprint

def chunk_text(full_text, chunks):  #inputs 1 page
	section_pattern = re.compile(r'^(\d+)\.\s+[A-Z]')

	lines = []	
	chunk = []

	for idx in range(len(full_text)):
			lines.append(full_text[idx]['text']) #breaks it into lines

	if not section_pattern.match(lines[0]) and chunks :     # check the first line to see if it is a continuation of last page
		last_key = next(reversed(chunks))
		chunk.extend(chunks[last_key])
		chunk.append(lines[0])
	else:
		chunk.append(lines[0])

		
	i = 1
	while i != len(lines):
		if section_pattern.match(lines[i]):  #use pattern '1. A' to chunk text
			if not chunk:
				chunk.append(lines[i])
				i+=1
			else:
				idx_of_dict = ''
				for n in chunk[0][0:3]:
					if n.isdigit():
						idx_of_dict += n 
				chunks[idx_of_dict] = chunk
				chunk = []
				chunk.append(lines[i])
				i+=1
		else:
			chunk.append(lines[i])
			i+=1

	idx_of_dict = ''           # anything left is added back to the dict to continue in the next run
	for n in chunk[0][0:3]:
		if n.isdigit():
			idx_of_dict += n 
	chunks[idx_of_dict] = chunk
	return chunks

chunks = {}
with plumber.open("./data/raw/bns.pdf") as pdf:
	page = pdf.pages[15]                  #start on page 16 of bns.pdf because everything before is not useful
	height = page.height
	width = page.width
	cropped = page.crop((0,0,width,height - 65))
	full_text = cropped.extract_text_lines()
	full_text.pop(-1)              #removing a footnote that only exist in the first page
	full_text.pop(-1)
	# print(full_text[-1]['text'])
	out = chunk_text(full_text,chunks)

	for i in range(16,110):
		page = pdf.pages[i]
		height = page.height
		width = page.width
		cropped = page.crop((0,0,width,height - 65)) #left,up,right,down

		full_text = cropped.extract_text_lines()
		out = chunk_text(full_text,chunks)
	pprint(chunks, indent=4)
