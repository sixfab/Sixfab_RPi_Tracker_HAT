from setuptools import setup, find_packages

setup(
    name='sixfab_gprsiot',
    version='1.0.0',
    author='Yasin Kaya',
    author_email='yasinkaya.121@gmail.com',
    description='sixfab python libraries',
    license='MIT',
    url='https://github.com/sixfab/Sixfab_RPi_Tracker_HAT',
    dependency_links  = [],
	install_requires  = ['pyserial','pigpio'],
    packages=find_packages()
)
