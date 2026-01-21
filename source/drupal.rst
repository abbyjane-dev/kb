==============
Drupal Install
==============

*************
Prerequisites
*************

Debian
======

Install the prerequisites. Most of these should already be installed. The command will only add the missing components not duplicate anything already existing.

.. code-block:: bash

    sudo apt update
    sudo apt install -y php-fpm php-cli php-xml php-mbstring php-gd php-curl php-zip php-mysql php-intl php-bcmath unzip git mariadb-server

Check PHP version and that FPM is running.

.. code-block:: bash

    php -v
    systemctl status php*-fpm --no-pager

Install Composer
================

This will install Composer system-wide.

.. code-block:: bash

    cd /tmp
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"

.. code-block:: bash

    php composer-setup.php


.. code-block:: text

    All settings correct for using Composer
    Downloading...

    Composer (version 2.9.3) successfully installed to: /tmp/composer.phar
    Use it: php composer.phar

.. code-block::bash

    sudo mv composer.phar /usr/local/bin/composer
    composer --version

.. code-block:: text

    Composer version 2.9.3 2025-12-30 13:40:17
    PHP version 8.4.11 (/usr/bin/php8.4)
    Run the "diagnose" command to get more detailed diagnostics output.

*************************
Set Up Drupal Environment
*************************

Create Drupal Directory
=======================

Create the directory

.. code-block:: bash

    mkdir /var/www/abbynet/drupal
    cd /var/www/abbynet/drupal

Create the project

.. code-block:: bash

    cd /var/www/abbynet/drupal
    composer create-project drupal/recommended-project:^10 .

Directory Permissions
=====================

Drupal will want this directory to exist before install

.. code-block:: bash

    sudo mkdir -p /var/www/abbynet/drupal/web/sites/default/files
    sudo chown -R www-data:www-data /var/www/abbynet/drupal/web/sites/default/files

Create Database
===============

.. code-block:: sql

    CREATE DATABASE drupal CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    CREATE USER 'drupaluser'@'localhost' IDENTIFIED BY 'use-a-long-password-here';
    GRANT ALL PRIVILEGES ON drupal.* TO 'drupaluser'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;

Caddy Site Block
================

.. code-block:: text

    drupal.cloverdalelane.com {
        root * /var/www/abbynet/drupal/web

        basic_auth {
            abby <password hash>
        }

        php_fastcgi unix//run/php/php8.4-fpm.sock
        file_server
    }


To find the php socket version:

.. code-block:: bash

    ls -l /run/php/

Reload Caddy
============

.. code-block:: bash

    sudo caddy validate --config /etc/caddy/Caddyfile
    sudo systemctl reload caddy

**************
Install Drupal
**************

Navigate to:

.. code-block:: html

    https://drupal.example.com

It should show the Drupal installer. Use the DB settings from earlier:

- Database: `drupal`
- Username: `drupaluser`
- Password: the one set
- Host: `localhost`

*************
Sanity Checks
*************

See if PHP is being executed:

.. code-block:: bash

    curl -I https://drupal.cloverdalelane.com

Check Caddy logs:

.. code-block:: bash

    journalctl -u caddy -n 100 --no-pager

Check php-fpm logs:

.. code-block:: bash

    journalctl -u php8.2-fpm -n 100 --no-pager
