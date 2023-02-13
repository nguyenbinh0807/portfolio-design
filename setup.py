from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

DISTNAME = 'design_portfolio'
INSTALL_REQUIRES = (
    ['pandas>=0.19.2', 'numpy>=1.20.2', 'plotly>=4.2.1', 'scipy>=1.2.0', 'vnstock', 'requests']
)

VERSION = '0.0.3'
LICENSE = 'MIT'
DESCRIPTION = 'Viet Nam stock profile'
AUTHOR = "nguyenthebinh"
EMAIL = "2054022009binh@ou.edu.vn"
URL = "https://github.com/nguyenbinh0807/profilevn.git"
DOWNLOAD_URL = "https://github.com/nguyenbinh0807/profilevn.git"

setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description = long_description,
      long_description_content_type = "text/markdown",
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license = LICENSE,
      #package name are looked in python path
      packages=find_namespace_packages(include=['design_portfolio', 'design_portfolio.*']),
      keywords=['markowitzvn', 'python'],
      classifiers=[
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        "Operating System :: OS Independent",
      ],
      install_requires=INSTALL_REQUIRES,
     )
