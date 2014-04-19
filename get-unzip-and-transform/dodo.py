from glob import glob
from subprocess import check_call

from doit.tools import run_once
from doit.tools import check_timestamp_unchanged

ZIPS = ['data.zip', 'data2.zip']

def task_getTheZip():
    for datazip in ZIPS:
        yield {
            'name': datazip,
            'targets': [datazip],
            'uptodate': [run_once],
            'actions': ['cp ../data.zip %s' % datazip] # would be a 'wget' in a different context
            }

def task_unzip():
    for datazip in ZIPS:
        folder = datazip.replace('.zip', '')
        target = folder + '/.created'
        yield {
            'name': datazip,
            'file_dep': [datazip],
            'targets': [target],
            'actions': [' rm -fr %s/* ; mkdir -p %s ; (cd %s && unzip ../%s) && date --rfc-3339=ns > %s' %
                        (folder,folder,folder,datazip,target) ]
            }


def transform(folder):
    for f in glob(folder+'/*.txt'):
        future = f + '.future'
        check_call(""" cat %s | sed 's@this is@this gonna be... wait for it... @g' > %s """ % (f, future), shell=True)

def task_transform():
    for datazip in ZIPS:
        folder = datazip.replace('.zip', '')
        unzipdep = folder + '/.created'
        yield {
            'name': folder,
            'file_dep': [unzipdep],
            # or, if "date" is replaced by "touch" above, one can use:
            # 'uptodate': [check_timestamp_unchanged(unzipdep)],
            'actions': [(transform, [folder])],
            }

