from setuptools import setup

setup(
    name="generics",
    version="0.0.1",
    description="Generic mixins/views for Django",
    long_description="Generic mixins/views for Django",
    keywords="django, views, forms, mixins",
    author="Jared Morse <jarcoal@gmail.com>",
    author_email="jarcoal@gmail.com",
    url="https://github.com/jarcoal/django-generics",
    license="BSD",
    packages=["generics"],
    zip_safe=False,
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)