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
