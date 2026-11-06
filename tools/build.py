import sys
import os; s=open(os.path.join(os.path.dirname(__file__), '..', 'src', 'index.src.html')).read()
i=s.index('<style>'); head=s[:i]; rest=s[i:]
j=rest.index('</style>')+len('</style>'); style=rest[:j]; body=rest[j:]
head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">','').strip()
out=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Kathan Prajapati: how I research, from understanding the business to conviction.">
<meta property="og:title" content="Kathan Prajapati">
<meta property="og:description" content="How I research, from understanding the business to conviction.">
<meta name="theme-color" content="#0A0B0D">
{head}
{style}
</head>
<body>
{body.strip()}
</body>
</html>
'''
open(sys.argv[1],'w').write(out)
