from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name='ragctl',
    version='0.1.0',
    description='A CLI tool for Retrieval Augmented Generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Devopcasting/RAGCLI',
    author='Prashant Pokhriyal',
    author_email='devopcasting@gmail.com',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'ragctl=ragctl.__main__:main',
        ],
    },
    platforms=["linux", "macos"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12',
    ],
)