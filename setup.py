from setuptools import find_packages, setup

import djangocms_fil_permissions


INSTALL_REQUIREMENTS = ["Django>=1.11,<2.0", "django-cms>=3.5.0", "rules"]


setup(
    name="djangocms-fil_permissions",
    packages=find_packages(),
    include_package_data=True,
    version=djangocms_fil_permissions.__version__,
    description=djangocms_fil_permissions.__doc__,
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    install_requires=INSTALL_REQUIREMENTS,
    author="Fidelity International",
    url="https://github.com/FidelityInternational/djangocms-fil_permissions",
    license="BSD",
    test_suite="tests.settings.run",
)
