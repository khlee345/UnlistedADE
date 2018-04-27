__author__ = 'Kahyun Lee'
__email__ = 'klee70@gmu.edu'

from lxml import etree as ET
import os,re 
import spacy

def xml_to_brat(fdir,fname):

	nlp = spacy.load('en')

	for file in os.listdir(fdir):
		label_text = ''
		lines = []
		tree = ET.parse(fdir+'/'+file)
		sections = tree.xpath('//Section/text()')
		mentions = tree.xpath('//Mention')
		span = {}
		sections_num = len(sections)
		section_len = 0
		for i in range(sections_num):
			for mention in mentions:
				if mention.get('section') == 'S'+str(i+1):
					try:
						span[int(mention.get('start'))+section_len] = (mention.get('type'),mention.get('len'),mention.get('str'))
					except:
						continue
			section_len = section_len+len(sections[i])
			label_text = label_text+sections[i]
		tokens = re.finditer(r'\S+', label_text)
		lines.append('-DOCSTART- -X- -X- O\n\n')
		token_list = []
		for token in tokens:
			token_list.append((token.group(0),token.start()))
		i=0
		while i < len(token_list):
			token_text = token_list[i][0]
			token_start = token_list[i][1]
			if token_start in span.keys():
				ent_tokens = nlp(span[token_start][2])
				ent_len = len(ent_tokens)
				ent_type = span[token_start][0]
				new_line = ent_tokens[0].text+' NN '+'B-'+ent_type+' '+'B-'+ent_type+'\n'
				lines.append(new_line)
				j=0
				if ent_len >= 2:	
					j = 1
					while j < ent_len: 
						add_line = ent_tokens[j].text+' NN '+'I-'+ent_type+' '+'I-'+ent_type+'\n'
						lines.append(add_line)
						j += 1
				i = i+len(span[token_start][2].split())
			else:
				ent_tokens = nlp(token_text)
				for ent_token in ent_tokens:
					new_line = ent_token.text+' NN O O'+'\n'
					lines.append(new_line)
				i += 1
		lines.append('\n')
		with open(fname,'a') as f:
			for line in lines:
				f.write(line)


if __name__ == '__main__':
	xml_to_brat('./Train','train.txt')