from common.imports import *

def clean():
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
def run():
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

