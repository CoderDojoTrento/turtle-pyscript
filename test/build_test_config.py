import os
import shutil
import glob
import json



demo_paths = ['main.py'] + sorted([fpath for fpath in glob.glob("demos/*.py")]) 
test_paths = sorted(   [fpath for fpath in glob.glob("test/uitest_*.py")]
                     + [fpath for fpath in glob.glob("test/stresstest_*.py")] )


print("Found demos paths", demo_paths)
print()

print("Found tests paths", test_paths)
print()

demo_names = [os.path.split(dp)[1][:-3] for dp in demo_paths]
test_names = [os.path.split(t)[1][:-3] for t in test_paths]



with open('test/pyscript-test-template.json', encoding='utf-8') as fconf_template:
    
    #TODO ADD CHECK
    with open('pyscript-test.json', 'w', encoding='utf-8') as fconf_out:
        jsonobj = json.load(fconf_template)
        files = jsonobj["files"]
        for test_path in test_paths:
            files[test_path] = ""
        json.dump(jsonobj,fconf_out, indent=4)
    print(f'Wrote pyscript-test.json')




print()
print()
print('DONE.')
print()
print()