Changelog
=========

0.5.4 - May 13 2016
-------------------
* bugfix for C version of damerau_levenshtein thanks to Tyler Sellon

0.5.3 - March 15 2016
---------------------
* style/packaging changes


0.5.2 - February 3 2016
-----------------------

* testing fixes for Python 3.5
* bugfix for Metaphone w/ silent H thanks to Jeremy Carbaugh

0.5.1 - July 12 2015
--------------------

* bugfixes for NYSIIS
* bugfixes for metaphone
* bugfix for C version of jaro_winkler

0.5.0 - April 23 2015
---------------------

* consistent unicode behavior, all functions take unicode and reject bytes on Py2 and 3, C and Python
* parametrize tests
* Windows compiler support

0.4.0 - March 27 2015
---------------------

* tons of new tests
* documentation
* split out cjellyfish
* test all w/ unicode and plenty of fixes to accommodate
* 100% test coverage

0.3.4 - February 4 2015
-----------------------

* fix segfaults and memory leaks via Danrich Parrol

0.3.3 - November 20 2014
------------------------

* fix bugs in damerau and NYSIIS

0.3.2 -  August 11 2014
-----------------------

* fix for jaro-winkler from David McKean
* more packaging fixes

0.3.1 - July 16 2014
--------------------

* packaging fix for C/Python alternative

0.3.0 - July 15 2014
--------------------

* python alternatives where C isn't available

0.2.2 - March 14 2014
---------------------

* testing fixes
* assorted bugfixes in NYSIIS

0.2.0 - January 26 2012
-----------------------

* incorporate some speed changes from Peter Scott
* segfault bugfixes.

0.1.2 - September 16 2010
-------------------------

* initial working release
