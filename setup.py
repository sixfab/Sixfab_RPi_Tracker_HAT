from setuptools import setup, find_packages

setup(
    name='sixfab_gprsiot',
    version='1.0',
    author='Yasin Kaya',
    author_email='yasinkaya.121@gmail.com',
    description='sixfab linux libraries',
    license='MIT',
    url='https://github.com/sixfab/Sixfab_RPi_GPRSIoT_HAT',
    dependency_links  = [],
	install_requires  = ['pyserial'],
    packages=find_packages()
)
