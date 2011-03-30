from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "purest",
        version = "0.1",
        packages = find_packages('src'),
        package_dir = {'': 'src'},
        include_package_data=True,
        zip_safe=False,
        url = 'https://github.com/crito/purest',
        license = "GPL v3",
        author = "Christo Buschek",
        author_email = "crito@30loops.net",
        description = "A thin WSGI wrapper to store and retrieve collectd data sets in couchdb",
        long_description = read('README'),
        install_requires = [ 'distribute', 'gunicorn', 'simplejson', 'couchdb' ],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP',
            ]
)
