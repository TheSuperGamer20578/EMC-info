.. EMC Info documentation master file, created by
   sphinx-quickstart on Wed Jun 30 19:07:01 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

************************************
Welcome to EMC Info's documentation!
************************************
.. toctree::
   :hidden:
   :glob:

   *

Installation
============
::

   pip install EMC-info

.. note::
   If you need to use the package asynchronously, you need to install it with the async option ::

      pip install EMC-info[async]

Usage
=====
Importing::

   import emc

Getting info about a town and printing its mayor's name::

   town = emc.Town("town")
   print(town.mayor.name)

See the :doc:`API Reference <APIReference>` for all the attributes and classes available

Data
----
Most classes accept a parameter named ``data``. This is so that you don't have to wait for it to get the data every time
you want to get info about something, you can get the value of the parameter with :func:`emc.util.get_data`

.. note::
   Use :func:`emc.async_.get_data` if you are using the package asynchronously.

::

   data = emc.util.get_data()
   town_a = emc.Town("town", data=data)
   town_b = emc.Town("other town", data=data)

Asynchronous usage
------------------
If you are using this package asynchronously you will need to manually get data using :func:`emc.async_.get_data`::

   town = emc.Town("town", data=await get_data())

.. note::
   You need to import :func:`emc.async_.get_data`::

      from emc.async_ import get_data

Help
====
If you get stuck, feel free to start a `discussion <https://github.com/TheSuperGamer20578/EMC-info/discussions>`_

If this documentation is missing something, open an `issue <https://github.com/TheSuperGamer20578/EMC-info/issues>`_
