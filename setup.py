from distutils.core import setup
import py2exe

setup(
    console=['src/main.py'],  # Specify your main script here
    data_files=[
        ('', ['src/gg.xlsx', 'src/qrdetector.ui',
         'src/README.md', 'src/requirements.txt'])
    ],
    options={
        'py2exe': {
            'packages': [],  # Exclude all packages
            'excludes': ['tkinter']  # Exclude 'tkinter' module if necessary
        }
    },
    zipfile=None  # Do not create a zipfile
)

# pip install py2exe
# python setup.py py2exe
