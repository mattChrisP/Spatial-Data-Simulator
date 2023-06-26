from setuptools import setup, find_packages

setup(
    name='glocator',
    version='0.1',
    description='Basic release',
    url='https://github.com/mattChrisP/Spatial-Data-Simulator',
    author='Matthew Christopher Pohadi',
    author_email='matthewchristopherpohadi@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'flask',
        'flask_cors',
        'rtree',
        'psycopg2',
        'python-dotenv',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    python_requires='>=3.6',
)