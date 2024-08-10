from setuptools import setup, find_packages

setup(
    name='ragctl',
    version='0.1.0',
    description='A CLI tool for Retrieval Augmented Generation',
    long_description=open('README.md').read(),
    url='https://github.com/Devopcasting/RAGCLI',
    author='Prashant Pokhriyal',
    author_email='devopcasting@gmail.com',
    license='MIT',
    packages=find_packages(where='src', exclude=['__pycache__']),
    package_dir={'': 'src'},
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'ragctl=src.reagctl:main',
        ],
    },
    platforms=["Linux", "MacOS"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12.3'
    ],
)