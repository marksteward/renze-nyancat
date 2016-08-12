#!/usr/bin/env python
import json
import os

files = json.load(open('nyancat.php'))

with open('nyanres.php') as packed:
	for i in range(len(files)):
		file = files['file%s' % i]
		print("Extracting %s for %s" % (file['name'], file['size']))

		outname = 'unpacked/' + file['name']
		outdir = os.path.dirname(outname)
		if not os.path.isdir(outdir):
			os.makedirs(outdir)

		with open(outname, 'w') as outfile:
			outfile.write(packed.read(file['size']))

	extra = packed.read()
	if extra:
		print('%s bytes extra: %r' % (len(extra), extra))

