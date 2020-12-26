import os


for f in os.listdir('.'):
    name, ext = os.path.splitext(f)
    if ext == '.png':
        num = int(f[5])
        os.rename(f,f[:5]+str(num+2)+f[6:])