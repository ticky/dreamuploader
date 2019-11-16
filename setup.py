from setuptools import setup

setup(name='dreamuploader',
      version='0.1.0',
      description='One-shot Dreamcast file upload server',
      url='http://github.com/ticky/dreamuploader',
      author='Jessica Stokes',
      author_email='hello@jessicastokes.net',
      license='MIT',
      python_requires='>3.7.0',
      packages=['dreamuploader'],
      scripts=['bin/dreamuploader'],
      install_requires=[
        'attrs',
        'django-htmlmin',
        'jinja2',
        'klein',
        'q',
        'twisted'
      ],
      include_package_data=True,
      zip_safe=False)
