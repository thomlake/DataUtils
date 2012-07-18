from distutils.core import setup

setup(
    name='DataUtils',
    version='0.1.0',
    author='tllake',
    author_email='thom.l.lake@gmail.com',
    packages=['datautils', 'datautils.samplers', 'datautils.wordembeddings'],
    #package_dir={'datautils':'datautils/'},
    package_data={'datautils':['data/*.txt']},
    license='LICENSE.txt',
    description='common data operations.',
    long_description=open('README.rst').read(),
)

