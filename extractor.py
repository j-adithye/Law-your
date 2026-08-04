import pdfplumber as plumber
import re
import json

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
				
				chunk[0] = chunk[0][len(idx_of_dict)+2:]
				chunks[idx_of_dict] = chunk
				chunk = []
				chunk.append(lines[i])
				i+=1
		else:
			chunk.append(lines[i])
			i+=1

	idx_of_dict = ''           # anything left is added back to the dict to continue in the next loop
	for n in chunk[0][0:3]:
		if n.isdigit():
			idx_of_dict += n 
	if not chunk[0][0].isdigit():
		chunk[0] = chunk[0][len(idx_of_dict)+2:]
	chunks[idx_of_dict] = chunk
	return chunks

def format_chunks(value):    # formats chunks to a clean structure
	formatted = ''
	subclass_pattern = re.compile(r'^\([A-Za-z0-9]+\)')
	for line in value:
		if subclass_pattern.match(line):
			formatted += '\n' + line
		else:
			formatted += ' ' + line

	return(formatted)

def to_json(chunks):
	with open("./data/processed/bns_sections.json", "w") as doc:
		json.dump(chunks, doc, indent=4)
		print("Set")

chunks = {}
with plumber.open("./data/raw/bns.pdf") as pdf:
	page = pdf.pages[15]                  #start on page 16 of bns.pdf because everything before is not useful
	height = page.height
	width = page.width
	cropped = page.crop((0,0,width,height - 65))
	full_text = cropped.extract_text_lines()
	full_text.pop(-1)              #removing a footnote that only exist in the first page
	full_text.pop(-1)
	out = chunk_text(full_text,chunks)

	for i in range(108,111):
		page = pdf.pages[i]
		height = page.height
		width = page.width
		cropped = page.crop((0,0,width,height - 65)) #left,up,right,down

		full_text = cropped.extract_text_lines()
		out = chunk_text(full_text,chunks)
chunks.pop('',None)


for key,value in chunks.items():
	formatted = format_chunks(value)
	chunks[key] = formatted

to_json(chunks)

