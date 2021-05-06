from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='shows',
    version='0.0.1',
    description='',
    url='https://github.com/voidful/shows',
    author='Voidful',
    author_email='voidful.stack@gmail.com',
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    setup_requires=['setuptools-git'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python"
    ],
    license="Apache",
    keywords='system monitoring gpu cpu network memory disk utility usage state',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': ['shows=shows.main:main']
    },
    zip_safe=False,
)
