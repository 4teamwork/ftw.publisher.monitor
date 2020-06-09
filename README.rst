ftw.publisher.monitor
=====================

This package is an `ftw.publisher`_ addon for monitoring the publisher
queue and alerting when the queue cannot be processed for some reason.


Usage
-----

- Add ``ftw.publisher.monitor`` to your buildout configuration on
  the **editoral site** and run ``bin/buildout``:

::

    [instance]
    eggs +=
        ftw.publisher.sender
        ftw.publisher.monitor

- Configure the report in the publisher control panel.


Failed extraction monitoring
----------------------------

When the publisher is set up with an asynchronous extraction queue (e.g. with redis),
the extraction may break.
This is possible because the extraction is asynchronous and thus not in the same
transaction as the publisher job is created.
Therefore creating the publisher job may work, but executing the extraction job may fail.

For mitigating that problem we are monitoring the jobs and warn whenever a job has still
a 0-sized job file and the job file is older than the configured threshold.


Upgrade 2.0
-----------

First you need to install the profile ``ftw.publisher.monitor:default``.
The profile hasn't existed before and because after the installation of a profile
all upgradesteps are shown as installed, you have to run it manually or have to
reenter the data in the config panel.


Links
-----

- github project repository: https://github.com/4teamwork/ftw.publisher.monitor
- Main publisher github project repository: https://github.com/4teamwork/ftw.publisher.sender
- Issues: https://github.com/4teamwork/ftw.publisher.monitor/issues
- Pypi: http://pypi.python.org/pypi/ftw.publisher.monitor
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.publisher.monitor


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.publisher.monitor`` is licensed under GNU General Public License, version 2.


.. _ftw.publisher: https://github.com/4teamwork/ftw.publisher.sender
