import os
import shutil
import glob
import json


demos_paths = sorted([fpath for fpath in glob.glob("demos/*.py")]) 
tests_paths = sorted([fpath for fpath in glob.glob("test/uitest_*.py")])

prj_paths = ['main.py'] + demos_paths + tests_paths
print("Found paths", prj_paths)
print()

demos_names = [os.path.split(dp)[1][:-3] for dp in demos_paths]
test_names = [os.path.split(t)[1][:-3] for t in tests_paths]

prj_names = ['main'] + demos_names + test_names
print("Found names", prj_names)
print()

def gen_iframe(prj_name):
    return f'''
    <div class="tps-test-preview">
        <a href="{prj_name}.html" target="_blank">Open</a>'

        <iframe src="{prj_name}.html" width="500" height="600">
        </iframe>
    </div>
    '''

iframes_list = [ gen_iframe(prj_name) for prj_name in prj_names ]

#print(iframes_list)


iframes = "\n".join(iframes_list)

all_tests_index = f"""

<!doctype html>

<html>
    <head>
        <!-- Recommended meta tags -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <title>Turtle Pyscript tests</title>
        <link rel="icon" type="image/png" href="./img/favicon.png" />
        <link rel="stylesheet" href="./css/turtleps-test.css" />
    </head>

    <body>
        <dialog id="loading">
            <h1>Loading...</h1>
        </dialog>
        <h1><a href="https://github.com/CoderDojoTrento/turtle-pyscript" target="_blank">Turtle Pyscript</a> tests, by <a href="https://www.coderdojotrento.it" target="_blank">CoderDojoTrento</a></h1>
        <h2>It may take sometime to load everything ...</h2>
        <div id="tpt-previews">
        {iframes}
        </div>
    </body>

</html>

"""


if os.path.exists('_build/test'): 
    print("Deleting", '_build/test/', '...')
    shutil.rmtree('_build/test')

print('Creating', '_build/test', '...')
os.makedirs('_build/test')

with open('_build/test/index.html','w', encoding='utf-8') as fall_tests_out:
    fall_tests_out.write(all_tests_index)

shutil.copytree('css', '_build/test/css')
shutil.copytree('img', '_build/test/img')

shutil.copytree('test/css', '_build/test/css', dirs_exist_ok=True)
shutil.copytree('test/img', '_build/test/img', dirs_exist_ok=True)


#shutil.copytree('demos', '_build/test/', dirs_exist_ok=True)

for fpath in prj_paths:
    shutil.copy(fpath, '_build/test/')
    #print('Wrote', '_build/test/{}')

shutil.copyfile('turtleps.py', '_build/test/turtleps.py')


for prj_name in prj_names:
    
    
    with open(f'index.html', encoding='utf-8') as ftest_html_in:
        test_index = ftest_html_in.read()

        with open(f'_build/test/{prj_name}.html','w', encoding='utf-8') as ftest_html_out:
            
            sout = test_index.replace('Turtle Pyscript', prj_name) \
                             .replace('main.py', f'{prj_name}.py')
            
            if prj_name in demos_names:
                extra_run = f"""<script type="py"  config="./pyscript.json">
                    await run()  
                </script>
                """
                #TODO DIRTY, PRONE TO BUGS
                sout = sout.replace('</section>',extra_run + '</section>') 
                
            ftest_html_out.write(sout)
            print('Wrote', f'_build/test/{prj_name}.html')


with open('pyscript.json', encoding='utf-8') as fpyscript_json:
    
    path = '_build/test'  # no trailing slash
    with open('_build/test/pyscript.json', 'w', encoding='utf-8') as fpyscript_json_out:
        jsonobj = json.load(fpyscript_json)
        jsonobj["packages"].append('pytest')
        jsonobj["files"][r"{PATH}/test/uitest_api.py"] = "uitest_api.py"
        json.dump(jsonobj,fpyscript_json_out, indent=4)
    print(f'Wrote {path}/pyscript.json')


"""
from turtleps import *
from tests import *


#test_lag()
await test_interactive_loop()

#await test_storytelling()
"""


print()
print()
print('DONE.')
print()
print()
print('    Tests are available at',"       https://127.0.0.1:8008/_build/test/   ")
print()
print()
