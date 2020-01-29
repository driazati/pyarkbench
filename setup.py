from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyarkbench',
    version='1.0.1',
    description='Benchmarking utilities',
    url='http://github.com/driazati/pyarkbench',
    author='driazati',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pyarkbench'],
    zip_safe=False,
)
