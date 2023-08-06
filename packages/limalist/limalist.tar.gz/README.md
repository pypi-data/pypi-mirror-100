Mist
====


        - Doxygen <https://www.geogebra.org/m/fprxd9wa>
		- Sphinx <https://www.geogebra.org/m/uyfx4ykb>
		- Breathe <https://www.geogebra.org/m/sdrubcuq>
		- sphinx_rtd_theme <https://www.geogebra.org/m/eakkj9dq>
		- sphsdinx_rtd_theme <https://www.geogebra.org/m/qgdnas6a>
		- Doxygen <https://www.geogebra.org/m/my5ejjej>
		- Sphinx <https://www.geogebra.org/m/qr9fvygv>
		- Breathe <https://www.geogebra.org/m/sku5uj9f>
		- sphinx_rtd_theme <https://www.geogebra.org/m/yba3bfmu>
		- sphsdinx_rtd_theme <https://www.geogebra.org/m/avbs3n5r>
		- sphsdinx_rtd_theme <https://www.geogebra.org/m/mrgnxj9p>






Run *cmake* with *BuildDocs* set to *ON*:

::

    mkdir /path/to/build
    cd /path/to/build
    cmake -DBuildDocs:BOOL=ON /path/to/mist
    make Sphinx

And then run the build as above.

For Developers
==============

This project follows the Pitchfork Layout (PFL).  Namespaces are encapsulated in separate directories. Any physical unit must only include headers within its namespace, the root namespace (core), or interface headers in other namespaces.  The build system discourages violations by making it difficult to link objects across namespaces.

Documentation for this project is dynamically generated with Doxygen and Sphinx. Comments in the source following Javadoc style are included in the docs. Non-documented comments, e.g. implementation notes, developer advice, etc. follow standard C++ comment style. This README and other documents should be written in the intersection of Markdown and reStructuredText <https://gist.github.com/dupuy/1855764> for best interoperability.

Credits
=======

Mist is written by Andrew Banman. It is based on software written by Nikita Sakhanenko. The ideas behind entropy-based functional dependency come from Information Theory research by David Galas, Nikita Sakhanenko, and James Kunert.

For copyright information see the LICENSE.txt file included with the source.
