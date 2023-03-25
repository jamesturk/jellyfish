Changelog
=========

0.10.0 - 25 March 2023
---------------------
* removed rarely-used `porter_stem` function, better implementations exist

0.9.0 - 7 January 2021
----------------------
* updated documentation available at https://jamesturk.github.io/jellyfish/
* support for Python 3.10+
* handle spaces correctly in MRA algorithm

0.8.9 - 26 October 2021
-----------------------
* fix buffer overflow in NYSIIS
* remove unnecessary/undocumented special casing of digits in Jaro-Winkler

0.8.8 - 17 August 2021
----------------------
* release fix to fix Linux wheel issue

0.8.7 - 16 August 2021
----------------------
* safer allocations from CJellyfish
* include aarch64 wheels

0.8.4 - 4 August 2021
---------------------
* fix for jaro winkler (cjellyfish#8)

0.8.3 - 11 March 2021
---------------------
* build changes
* include OSX and Windows wheels

0.8.2 - 21 May 2020
-------------------
* fix jaro_winkler/jaro_winkler_similarity mix-up
* deprecate jaro_distance in favor of jaro_similarity
  backwards compatible shim left in place, will be removed in 1.0
* (note: 0.8.1 was a broken release without proper C libraries)

0.8.0 - 21 May 2020
-------------------
* rename jaro_winkler to jaro_winkler_similarity to match other functions
  backwards compatible shim added, but will be removed in 1.0
* fix soundex bug with W/H cases, #83
* fix metaphone bug with WH prefix, #108
* fix C match rating codex bug with duplicate letters, #121
* fix metaphone bug with leading vowels and 'kn' pair, #123
* fix Python jaro_winkler bug #124
* fix Python 3.9 deprecation warning
* add manylinux wheels

0.7.2 - 5 June 2019
-----------------------
* fix CJellyfish damerau_levenshtein w/ unicode, thanks to immerrr
* fix final H in NYSIIS
* fix issue w/ trailing W in metaphone

0.7.1 - 10 January 2019
-----------------------
* restrict install to Python >= 3.4

0.7.0 - 10 January 2019
-----------------------
* drop Python 2 compatibility & legacy code
* add bugfix for NYSIIS for words starting with PF

0.6.1 - April 16 2018
---------------------
* fixed wheel release issue

0.6.0 - April 7 2018
--------------------
* fix quite a few bugs & differences between C/Py implementations
* add wagner-fischer testdata
* uppercase soundex result
* better error handling in nysiis, soundex, and jaro

0.5.6 - June 23 2016
--------------------
* bugfix for metaphone & soundex raising unexpected TypeErrors on Windows (#54)

0.5.5 - June 21 2016
--------------------
* bugfix for metaphone WH case

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
