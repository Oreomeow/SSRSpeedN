import os.path

from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))

setup(
    name="ssrspeed",
    version="1.4.3",
    keywords=["ssr", "speed", "test"],
    url="https://github.com/OreosLab/SSRSpeedN",
    license="GPL-3.0 License",
    description="A simple tool to test nodes.",
    long_description=open(
        file=os.path.join(this_directory, "README.md"),
        mode="r",
        encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["ssrspeed.*"]),
    include_package_data=True,
    python_requires=">=3.8.0",
    install_requires=open(
        os.path.join(this_directory, "requirements.txt"),
        mode="r",
        encoding="utf-8"
    ).readlines(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["ssrspeed = ssrspeed.__main__:main"]},
)
