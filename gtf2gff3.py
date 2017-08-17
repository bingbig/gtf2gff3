#!/usr/bin/python
"""
Convert ensemble gtf to gff3 for JBrowse
Copyright (C)
__Author__: liubing
"""

import sys
import re

chr = 'chr'
keep_features = ["CDS", "UTR", "exon", "gene", "transcript"]

if len(sys.argv) < 2:
	print("Run:\n\tpython " + sys.argv[0] + " input.gtf output.gff3")
	exit()

gtf_file = sys.argv[1]
if len(sys.argv) == 2:
	gff_file = gtf_file.rstrip('gtf') + 'gff3'
else:
	gff_file = sys.argv[2]

### Parse gtf file
gtf = open(gtf_file, 'r')
gff = open(gff_file, 'w')

gtf_lines = gtf.readlines()
for line in gtf_lines:
	if re.match(r'^#', line):
		continue
	featureline = line.strip().split('\t')
	[seq, source, feature, start, end, score, strand, frame, attributes] = featureline
	if feature not in keep_features:
		continue

	seq = chr + seq
	if feature == 'transcript':
		feature = 'mRNA'

	attributes_array = attributes.replace('"','').strip(';').split('; ')
	
	if feature == 'gene':
		ID = str(attributes_array[0].split()[1])
		count = 0
		Name = attributes_array[1].split()[1]
		gff.write(
			'\t'.join([seq, source, feature, start, end, score, strand, frame]) + '\t' + 
			'ID=' + ID + ';Name='+Name +'\n')
	elif feature == 'mRNA':
		count += 1
		Parent = ID
		ID = str(attributes_array[0].split()[1])
		ID = ID + '.' + str(count)
		Name = Name + '.' + str(count)
		gff.write(
			'\t'.join([seq, source, feature, start, end, score, strand, frame]) + '\t' + 
			'ID=' + ID + ';Parent='+ Parent +';Name='+Name +'\n')
	else:
		gff.write(
			'\t'.join([seq, source, feature, start, end, score, strand, frame]) + '\t' + 
			'Parent=' + ID + '\n')

gff.close()
gtf.close()



	


