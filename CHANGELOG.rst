Change Log
==========

..
   All enhancements and patches to ecommerce_extensions will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.
Unreleased
----------

[1.2.1] - 2021-05-12
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Sentry configurations on apps.py


[1.2.0] - 2021-05-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Blocks of scripts in context_processors from THEME OPTIONS in tenant options.
* Blocks of HTML in context_processors from THEME OPTIONS in tenant options.


[1.1.0] - 2021-04-06
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* returning messages for debug with the 400 responses


[1.0.2] - 2021-02-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* using get since the object is a dict


[1.0.1] - 2021-02-18
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* correcting the KeyError


[1.0.0] - 2021-02-09
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add new payment processor (ednx-pp).

Fixed
_____

* Remove api key from parameters dictionary in Payu.


[0.3.0] - 2020-11-18
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Fomopay payment processor.

Fixed
_____

* Payu urls.

[0.2.0] - 2020-11-12
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Payu payment processor.


[0.1.0] - 2020-10-21
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Initial version
