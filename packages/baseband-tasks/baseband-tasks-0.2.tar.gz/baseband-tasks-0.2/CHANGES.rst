0.2 (2021-03-29)
================

This release depends on ``baseband`` 4.0 as this allows us to assume
(and document) the existence of ``baseband.tasks``.  Like baseband 4.0,
it requires python 3.7, astropy 4.0, and numpy 1.17.

New Features
------------

- Streams can now be sliced, returning a new stream for a more limited
  time span and/or sample shape. [#192]

- Streams can be turned into arrays by calling ``np.asarray(stream)``.
  No sanity check on amount of memory is done. [#194]

- ``SetAttribute`` can now also be used to change ``samples_per_frame``,
  ``shape`` or ``dtype``. [#195]

- All streams now have useful ``repr``. For tasks, this includes information
  on the underlying streams. [#198]

- The Noise generator has been upgraded to the ``Philox`` bit generator, which
  can be reset to a previous count.  This means that noise streams no longer
  need to carry state information for every frame, and that they are now
  independent of the order in which frames are initially accessed.  [#209]

API Changes
-----------

- For consistency with usage everywhere else, the ``polarization`` argument
  for ``Power`` and ``Square`` now refers to the output  polarization.
  This allows it to be set to whatever the user wants. [#198]

Bug Fixes
---------

- Time will now be reported correctly also for ``Stack`` and ``Integrate``
  even if their sample rate is not in Hz. Times will be accurate to the
  nearest sample of the underlying stream. [#197]

- Fix bug where times just on the border of polycos sometimes were wrongly
  considered outside of the valid range. [#206]

Other Changes and Additions
---------------------------

- Tasks can now be defined with a number of complete samples (``shape[0]``)
  that is not an integer multiple of ``samples_per_frame``, which can be
  used to avoid losing ends of streams for tasks that can handle dealing
  with partial frames. [#188]

0.1.1 (2020-07-19)
==================

Update that includes the DOI and for which the README.txt is clean
enough for ``twine``.


0.1 (2020-07-19)
================

Initial release.  Project renamed from original ``scintillometry``,
but similar in that the documentation still suggests that tasks be
imported from the various modules in ``baseband_tasks``, which is
the only way they can be used for ``baseband`` prior to 4.0.
