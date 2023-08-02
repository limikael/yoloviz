from setuptools import setup, find_packages
setup(
   name='yoloviz',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'ultralytics',
      'pygame',
      'click'
   ],
   entry_points='''
      [console_scripts]
      yoloviz=yoloviz:yoloshow_cli
      ''',
)