from setuptools import setup, find_packages

setup(
    name='rest_api_oscar',
    version='0.0.1',
    description='Code for a RESTful OSCAR API based on Flask-RESTPlus',
    url='https://github.com/kurt-hectic/oscar_rest_api',
    author='Timo Proescholdt',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.12.1', 'Flask-SQLAlchemy==2.3.1',],
    
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    
)