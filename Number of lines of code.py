from glob import glob
python = glob('*.py')

lines = 0
for file in python:
    with open(file) as f:
        lines += sum([line.strip() != "" and not line.startswith('#') for line in f]) 

html = glob('website/templates/*.html')
for file in html:
    with open(file) as f:
        lines += sum([line.strip() != "" and not line.startswith('') for line in f]) 
        
csv = glob('data/*.csv')
for file in csv:
    with open(file) as f:
        lines += sum([line.strip() != "" and not line.startswith('#') for line in f]) 

print("{} code lines in {} files.".format(lines, len(python) + len(html)))