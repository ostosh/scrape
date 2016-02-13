from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.0.1'

install_requires = [

]


setup(name='scrape',
    version=version,
    description="a protocol agnostic python scraper",
    long_description=README + '\n\n' + NEWS,
    classifiers=[

    ],
    keywords='',
    author='gostosh',
    author_email='ostoshg@gmail.com',
    url='github.com/ostosh/scrape',
    license='',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['scrape=scrape:main']
    }
)
