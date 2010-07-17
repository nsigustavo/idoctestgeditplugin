:Author: Gustavo Rezende <nsigustavo@gmail.com>

Doctest interactive Plugin
==========================

The idoctestgeditplugin searches for pieces of text that look like Python interactive sessions, and then executes these sessions.

Use <Shift><Enter> to activate the snippet and see a returned code in the document.

Example::

    >>> 1 + 1 # click shift+enter
    2         #      <-| and returned



Install
=======

::

    $ wget http://github.com/nsigustavo/idoctestgeditplugin/tarball/master
    $ tar -xzvf nsigustavo-idoctestgeditplugin*.tar.gz
    $ cd nsigustavo-idoctestgeditplugin*
    $ mv *  ~/.gnome2/gedit/plugins/


In gedit main menu go to: Edit -> Preferences

In Preferences dialog go to Plugins tab

Find 'interactive doctest' in plugin list and check it


Getting involved !
==================

idoctestgeditplugin's development may be viewed and followed on github::

  http://github.com/nsigustavo/idoctestgeditplugin


Retrieve the source code using git::

    $ git clone git://github.com/nsigustavo/idoctestgeditplugin.git

