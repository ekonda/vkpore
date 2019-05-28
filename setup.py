#!/usr/bin/env python3

from distutils.core import setup


with open('README.md', "r") as f:
    long_description = f.read()


setup(
    name='vkpore',
    version='0.0.2',
    description='Library for organizing interactions with Vkontakte api. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["library", "vkontakte", "asynchronous", "asyncio", "longpoll"],
    url='https://github.com/ekonda/vkpore/',
    author='Michael Krukov',
    author_email='krukov.michael@ya.ru',
    packages=['vkpore', 'vkpore.events', 'vkpore.objects'],
    install_requires=[
        'aiohttp',
    ],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
    ]
)
