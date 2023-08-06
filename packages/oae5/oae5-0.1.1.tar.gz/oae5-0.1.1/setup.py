from setuptools import setup, find_packages

setup(name="oae5",
      version="0.1.1",
      description=u"Package for educational purposes :)",
      url="",
      author="Miguel López Cruz -- lobolc --",
      author_email="",
      license="MIT",
      packages=find_packages(),
      install_requires = [
                          "sympy",
                          "numpy",
                          "pandas",
                          "matplotlib",
                          "ipython"
                          ],
      )
