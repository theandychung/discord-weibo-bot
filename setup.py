from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name="discord-weibo-bot",
    version='0.0.1',
    description="A discord bot which fetches the most "
                "recent weibo posts to discord through webhook",
    url='https://github.com/theandychung/discord-weibo-bot/',
    classifiers=[
        "License :: OSI Approved :: MIT License"
        "Programming Language :: Python :: 3.7",
    ],
    keywords="discord bot weibo",
    author="theandychung",
    author_email="theandychung@gmail.com",
    license="MIT",
    package=['discord-weibo-bot'],
    long_description=open('README.md').read(),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)