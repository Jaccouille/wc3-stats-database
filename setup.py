from setuptools import setup, find_packages

setup(name="wc3-stats-database",
      version='0.1',
      packages=find_packages(),
      description=("a scheduler to fetch stats from wc3stats.com API and save "
                   "them in a database"),
      entry_points={'console_scripts': ['start-scheduler = src.main:main']},
      author="Jaccouille",
      author_email='j4ccouille@gmail.com',
)
