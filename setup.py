from distutils.core import setup
import glob

setup(name='blog',
      version='1.0',
      description='blog project',
      author='Zoes',
      author_email='1162997984@qq.com',
      url='',
      packages=['blog', 'post', 'user'],
      py_modules=['manage'],
      data_files=['requirements'] + glob.glob('templates/*.html')
     )


