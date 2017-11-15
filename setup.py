import setuptools

setuptools.setup(
    name="deep_converter",
    version="0.1.0",
    url="https://github.com/victorusachev/deep_converter",

    author="Victor Usachev",
    author_email="usachev-1991@yandex.ru",

    description="Converts images to PDF, recursively processes the archives",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
