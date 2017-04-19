from setuptools import setup, find_packages

import m2mb


setup(
    name="m2mb",
    version=m2mb.__version__,
    description="Mail to Mattermost Bridge",
    long_description="""
This is a server for SMTP and related protocols, similar in utility to the
standard library's smtpd.py module, but rewritten to be based on asyncio for
Python 3.""",
    author="https://github.com/thperret",
    url="https://github.com/thperret/m2mb",
    keywords="email,chat,slack,mattermost",
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3+",
    zip_safe=False,
    python_requires="==3.6.*",
    #  setup_requires=[
        #  "aiosmtpd",
        #  ],
    install_requires=[
        "aiosmtpd==1.0a5",
        "requests",
        "sifter==0.1",
        ],
    dependency_links=[
        "git+https://github.com/thperret/aiosmtpd.git@auth#egg=aiosmtpd-1.0a5+auth",
        "git+https://github.com/thperret/sifter.git@python3#egg=sifter-0.1+py3",
        ],
    tests_require=[
        "aiohttp",
        ],
    entry_points={
        "console_scripts": ["m2mbd = m2mb.main:main"],
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: Email :: Mail Transport Agents",
        "Topic :: Communications :: Chat",
    ],
)
