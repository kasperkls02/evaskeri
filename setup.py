from setuptools import setup, find_packages

setup(
    name='nortec',
    version='0.3',
    packages=find_packages(),
    py_modules=["nortec"],
    description='A Python package for retrieving data from Nortec/Evaskeri backend',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kasper Læssø Sørensen',
    author_email='kasper@laessoerensen.dk',
    url='https://github.com/kasperkls02/nortec',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
)