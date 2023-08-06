from setuptools import setup, find_packages

extras_require = [
    'ray[rllib,debug]==0.7.3',
    'tensorflow==1.13.0rc1',
    'pillow==6.1.0',
    'pandas==0.25.0',
    'requests==2.22.0',
    'configspace==0.4.10',
    'scipy==1.3.0',
    'pandas==0.25.0',
]

extras_require_cont = [
    # 'ray[rllib,debug]==0.9.0',
    'tensorflow==2.2.0',
    'tensorflow-probability==0.9.0',
    'pandas==0.25.0',
    'requests==2.22.0',
    'mujoco-py==2.0.2.13', # with mujoco 2.0
    'configspace==0.4.10',
    'scipy==1.3.0',
    'pandas==0.25.0',
]

AUTHORS = ', '.join(["Raghu Rajan", "Jessica Borja",
                     "Suresh Guttikonda", "Fabio Ferreira"
                     "André Biedenkapp", "Frank Hutter"
                     ]),

AUTHOR_EMAIL = 'rajanr@cs.uni-freiburg.de'

LICENSE = 'Apache License, Version 2.0'


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mdp_playground',
    version='0.0.1',
    author=AUTHORS,
    author_email=AUTHOR_EMAIL,
    description="A python package to design and debug RL agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/RaghuSpaceRajan/mdp-playground",
    project_urls={
    "Bug Tracker": "https://github.com/RaghuSpaceRajan/mdp-playground/issues",
    },
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    # 'Topic :: Scientific/Engineering :: Machine Learning',
    # 'Topic :: Scientific/Engineering :: Reinforcement Learning', invalid classifiers on Pypi
    ],
    # package_dir={"": "src"},
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['gym'],
    extras_require={
      'extras_disc': extras_require,
      'extras_cont': extras_require_cont,
    },
)
