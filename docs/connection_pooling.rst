.. _database_connections:

Database connections
====================

This page describes the behaviour around database connections for Django applications running
with the uWSGI web server. uWSGI can be run with a number of processes and a number of threads (per process).

Django
------

**Default behavior:**

Each thread has its own database connection.
With 4 processes and 4 threads, there are a total of 16 threads, so 16 connections.

Persistent connections
----------------------

With this setting, database connections remain open for a certain amount of time, instead of opening a new connection for each request and then closing it afterwards.

- **DB_CONN_MAX_AGE**

  - ``0`` = Close connection after each request
  - ``None`` = Connections remain open indefinitely
  - ``60`` = Connections remain open for 60 seconds (default behaviour)

If ``DB_CONN_MAX_AGE=60``, there will be a maximum of 16 connections kept open for 60 seconds.

Connection pooling
------------------

``open-api-framework`` allows for database connection pooling (through Django 5.2 and the psycopg3 library),
which is configurable through environment variables.

.. note::

    The environment variables for connection pooling (such as ``DB_POOL_MIN_SIZE``) apply for
    **each** uWSGI process and the behavior of the connection pool might be slightly different then expected
    dependent on the number of processes and threads that are used by uWSGI, below are some
    different configurations and the expected number of maximum connections per configuration.

- **DB_POOL_ENABLED**

  - ``1`` = On
  - ``0`` = Off (default)

- **DB_POOL_MIN_SIZE**

  - ``4`` = default

- **DB_POOL_MAX_SIZE**

  - ``None`` = Use ``DB_POOL_MIN_SIZE``
  - ``<number>`` = Maximum number of connections in the pool

Creates a pool at the process level. Each thread connects to the process-level database pool.

When a process is “touched” (starts handling a request) the pool is created, typically with ``min_size`` or ``min size + 1``.
Initially you often see ``min size + 1`` connections, and under load, that number multiplied by the number of processes that are running.

If a process restarts, the pool managed by that pool is removed and will only be recreated once the process starts handling a new request.

**Expected maximum connection for different configurations**

A configuration like the one shown below is probably the best when using connection pooling,
because this allows limiting the maximum number of connections without having to lower the
number of threads.

``DB_POOL_MIN_SIZE`` = ``DB_POOL_MAX_SIZE`` < ``UWSGI_THREADS``

    * ``DB_POOL_MIN_SIZE``: 5
    * ``DB_POOL_MAX_SIZE``: 5
    * ``UWSGI_PROCESSES``: 4
    * ``UWSGI_THREADS``: 6 -> 20 conns

    **Maximum connections**: number of processes * min_size = 20 connections

The configuration below is valid, but probably not very useful in practice, because in this
case the maximum number of connections is the same as when running with connection pooling turned off.

``DB_POOL_MIN_SIZE`` <= ``UWSGI_THREADS`` <= ``DB_POOL_MAX_SIZE``:

    * ``DB_POOL_MIN_SIZE``: 2
    * ``DB_POOL_MAX_SIZE``: 8
    * ``UWSGI_PROCESSES``: 4
    * ``UWSGI_THREADS``: 5

    **Maximum connections**: number of processes * number of threads = 20 connections

The configuration below is valid, but probably not very useful in practice, because in this
case there will be a few connections that are never actually used under concurrency, because there isn't an
appropriate number of threads to make use of all of them.

``UWSGI_THREADS`` < ``DB_POOL_MIN_SIZE`` < ``DB_POOL_MAX_SIZE``

    * ``DB_POOL_MIN_SIZE``: 6
    * ``DB_POOL_MAX_SIZE``: 8
    * ``UWSGI_PROCESSES``: 4
    * ``UWSGI_THREADS``: 5

    **Maximum connections**: number of processes * (min_size + 1) = 28 connections

The configuration below is valid, but probably not very useful in practice, because in this
case there will be a few connections that are never actually used under concurrency, because there isn't an
appropriate number of threads to make use of all of them.

``UWSGI_THREADS`` < ``DB_POOL_MIN_SIZE`` = ``DB_POOL_MAX_SIZE``

    * ``DB_POOL_MIN_SIZE``: 8
    * ``DB_POOL_MAX_SIZE``: 8
    * ``UWSGI_PROCESSES``: 4
    * ``UWSGI_THREADS``: 5

    **Maximum connections**: number of processes * min_size = 32 connections
