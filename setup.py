from setuptools import setup, find_packages

setup(
    name='youtubetogo',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytube',
        'python-dotenv',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'youtubetogo=main:main',
        ],
    },
    author='kdcllc',
    author_email='info@kingdavidconsulting.com',
    description='A script to download and convert YouTube videos to either video or audio format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kdcllc/youtubetogo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
