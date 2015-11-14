Cleansweep customizations for Karnataka
=======================================

This repository is a cleansweep plugin, that provides required customizations for karnataka.

Customizations provide are:

* Custom signup form

How to run
----------

* Setup a cleansweep instance

* Install cleansweep-karnataka in the virtualenv by running:
    
    python setup.py develop

* edit config/development.conf in cleansweep and add the following line:

    PLUGINS = ['cleansweep_karnataka']

* run the cleansweep server using:

    python manage.py runserver
