from setuptools import setup, find_packages
import os

version = __import__('rat').__version__

install_requires = [
    'setuptools',
]

setup(
    name = "django-rat",
    version = version,
    url = 'http://github.com/ojii/django-rat',
    license = 'BSD',
    platforms=['OS Independent'],
    description = "An app to manage egg translations in buildout projects.",
    author = 'Jonas Obrist',
    author_email = 'ojiidotch@gmail.com',
    packages=find_packages(),
    install_requires = install_requires,
    package_data={
        '': ['*.txt', '*.rst',],
    },
    package_dir = {
        'rat':'rat',
    },
    zip_safe=False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
