### Speed Testing


    $ mkvirtualenv -p python2 jf2
    (jf2)$ pip install unicodecsv; python setup.py develop
    (jf3)$ python timedruns.py > python2.csv

    $ mkvirtualenv -p python3 jf3
    (jf3)$ python setup.py develop
    (jf3)$ python timedruns.py > python3.csv
