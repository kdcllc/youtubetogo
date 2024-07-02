from setuptools import setup, find_packages

setup(
    name='YouTubeToGo',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytube',
        'python-dotenv',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'YouTubeToGo=main:main',
        ],
    },
    author='kdcllc',
    author_email='info@kingdavidconsulting.com',
    description='A script to download and convert YouTube videos to either video or audio format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kdcllc/YouTubeToGo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
