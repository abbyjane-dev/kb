=================
Nginx Guide
=================

.. toctree::
    :maxdepth: 4

***************
Beginning Nginx
***************

This section explains the initial installation of Nginx and how to set up rudimentary web sites.

All examples use::
    * Linux server with sudo access
    * Domain: example.com
    * Web root: /var/www/
    * Nginx config dir: /etc/nginx/

Initial Nginx Install
=====================

On Debian/Ubuntu:

.. code-block:: bash

    sudo apt update && sudo apt upgrade
    sudo apt install nginx

Check that it is running:

.. code-block:: bash

    systemctl status nginx

You should see it as 'active(running)'.

If you are using a firewall (UFW):

.. code-block:: bash

    sudo ufw allow 'Nginx Full'
    sudo ufw enable

How sites-available/sites-enabled work
======================================

Key paths:
    * **Main config:** ``/etc/nginx/nginx.conf``
    * **Site configs (disabled or drafts):** ``/etc/nginx/sites-available``
    * **Enabled sites (actually used)** ``/etc/nginx/sites-enabled``

Important convention:
    * You create/edit virtual host ('server block') files in ``sites-available/``.
    * You enable them by making a symlink into ``sites-enabled/``.
    * Nginx only loads what is in ``sites-enabled/``.


Create a Web Root for the Domain
================================

Make a directory for example.com:

.. code-block:: bash

    sudo mkdir -p /var/www/example/

Give it an index page:

.. code-block:: bash

    echo "<h1>Hellow from example.com<h1> | sudo tee /var/www/example/index.html

Set permissions. There are two common paths.

Option A: Owned by Nginx user (www-data)

.. code-block:: bash

    sudo chown -R www-data:www-data /var/www/example/
    sudo chmod -R 755 /var/www/example/

You will need to ``sudo`` when editing.

Option B: Owned by our user

If you want to edit files without ``sudo``:

.. code-block:: bash

    sudo chown -R $USER:$USER /var/www/example
    sudo chmod -R 755 /var/www/example

Replace ``$USER`` with your username if copying into static docts.

Create a Server Block for the Domain
====================================

Create ``/etc/nginx/sites-available/example.com``:

.. code-block:: bash

    sudo nano /etc/nginx/sites-available/example

Example config:

.. code-block:: nginx

    server {
        listen 80;
        listen [::]:80;

        server_name example.com www.example.com;

        root /var/www/example;
        index index.html index.htm;

        access_log /var/log/nginx/example.access.log;
        error_log  /var/log/nginx/example.error.log;

        location / {
            try_files $uri $uri/ =404;
        }
    }

**Keys to making this work:**

    * ``server_name``: the domain nammes this block handles.
    * ``root``: path to your site files.
    * ``try_files``: only serve existing files/directories, otherwise 404.


Enable the Site
===============

Create a symlink in ``sites-enabled``:

.. code-block:: bash

    sudo ln -s /etc/nginx/sites-available/example /etc/nginx/sites-enabled/

.. hint::

    Use ``ln -s`` **from** ``sites-available`` **to** ``sites-enabled``, not the other way round.

Cleanup
=======

Disable the default site (optional but recommended)

.. code-block:: bash

    sudo rm /etc/nginx/sites-enabled/default

Test and reload Nginx

.. code-block:: bash

    sudo nginx -t
    sudo systemctl reload nginx

Now assuming DNS is set correctly, ``http://example.com`` should show your HTML.

*******************
Ongoing Maintenance
*******************

DNS Setup
=========

On your DNS provider's control panel:
    * Create an **A record** for ``example.com`` pointing to your server's IP address.
    * Optionally create ``www`` as an CNAME:
        Example:
            * ``example.com A 203.0.113.10``
            * ``www CNAME example.com``
        For a subdomain like ``blog.example.com``:
            * ``blog CNAME example.com``

.. note:: DNS changes can take a while to propagate.

Adding a New Subdomain
======================

Adding ``blog.example.com`` as a separate site, with its own files.

Create the web root
-------------------

.. code-block:: bash

    sudo mkdir -p /var/www/blog/
    echo "<h1>Hello from blog.example.com</h1>" | sudo tee /var/www/blog/index.html
    sudo chown -R $USER:$USER /var/www/blog/
    sudo chmod -R 755 /var/www/blog/

Create a server block
---------------------

Create ``/etc/nginx/sites-available/blog``:

.. code-block:: bash

    sudo nano /etc/nginx/sites-available/blog.example.com

Example config:

.. code-block:: nginx

    server {
        listen 80;
        listen [::]:80;

        server_name blog.example.com;

        root /var/www/blog;
        index index.html index.htm;

        access_log /var/log/nginx/blog.access.log;
        error_log  /var/log/nginx/blog.error.log;

        location / {
            try_files $uri $uri/ =404;
        }
    }

Enable and reload
-----------------

.. code-block:: bash

    sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx

Now ``http://blog.example.com`` should serve its own content.

Redirecting ``www`` → bare domain (optional)
============================================

If you want all traffic for ``example.com`` to redirect to ``www.example.com``:

One approach is:
    * Main site handles ``example.com``.
    * A tiny redirect server handles ``www.example.com``.

Example:

.. code-block:: nginx

    # /etc/nginx/sites-available/example.com
    server {
        listen 80;
        listen [::]:80;

        server_name example.com;

        root /var/www/example;
        index index.html index.htm;

        location / {
            try_files $uri $uri/ =404;
        }
    }

    server {
        listen 80;
        listen [::]:80;
        server_name www.example.com;

        return 301 http://example.com$request_uri;
    }

.. note:: Don't forget to test and reload.


HTTPS with Let’s Encrypt (Certbot) – Optional
=============================================

Install Certbot
---------------

On Debian/Ubuntu (using ``certbot`` snap is currently recommended):

.. code-block:: bash

    sudo snap install core
    sudo snap refresh core
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot

(Or use your distro's package manager if you prefer.)

Obtain and install certificate
------------------------------

Make sure your site is working over HTTP first and DNS is correct.

Then run (for ``example.com`` + ``www.example.com``):

..code-block:: bash

    sudo certbot --nginx -d example.com -d www.example.com

For a subdomain such as ``blog.example.com``:

.. code-block:: bash

    sudo certbot --nginx -d blog.example.com

Certbot will:
    * Prove you own the domain using HTTP challenges.
    * Edit your Nginx config to add ``listen 443 ssl`` blocks.
    * Set up automatic renewal.

Automatic Renewal
-----------------

Certbot typically installs a systemd timer or crong job. You can dry-run:

.. code-block:: bash

    sudo certbot renew --dry-run

***************
Common Pitfalls
***************

If something isn't working, run down this list.

* Did you put the config in ``sites-available`` AND symlink to ``sites-enabled``?
    * Check with:

    .. code-block:: bash

        ls -l /etc/nginx/sites-available
        ls -l /etc/nginx/sites-enabled

* Did you run ``sudo nginx -t`` before reloading?
    * If not, you might have syntax errors stopping Nginx from reloading.

* **Did you reload Nginx after changes?**

.. code-block:: bash
    
    sudo systemctl reload nginx

* Is DNS pointing to the correct server IP?
    * Use ``dig example.com`` or ``nslookup example.com`` from your local machine.

* Is the firewall open on ports 80 and 443?
    * On Ubuntu: ``sudo ufw status``

* Is the server_name correct?
    * Mis-typed server_name means Nginx may serve the wrong site or the default.

* Is the root directory correct and readable?
    * Check the path exists and your ``index.html`` is there.

* Access and error logs
    * Check logs to see what’s happening:
    
    .. code-block:: bash

        sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log


    * Or use the domain-specific logs if you configured them.

********
Template
********

For a new site or subdomain, you can mostly follow this pattern:

* **Create web root:**

.. code-block:: bash

    sudo mkdir -p /var/www/SITE_NAME/html
    sudo chown -R $USER:$USER /var/www/SITE_NAME
    sudo chmod -R 755 /var/www/SITE_NAME
    echo "<h1>Hello from SITE_NAME</h1>" | sudo tee /var/www/SITE_NAME/html/index.html


* **Create config:**

.. code-block:: bash

    sudo nano /etc/nginx/sites-available/SITE_NAME

.. code-block:: nginx

    server {
        listen 80;
        listen [::]:80;

        server_name YOUR_DOMAIN_HERE;

        root /var/www/SITE_NAME/html;
        index index.html index.htm;

        access_log /var/log/nginx/SITE_NAME.access.log;
        error_log  /var/log/nginx/SITE_NAME.error.log;

        location / {
            try_files $uri $uri/ =404;
        }
    }


* **Enable + reload:**

.. code-block:: bash

    sudo ln -s /etc/nginx/sites-available/SITE_NAME /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx


* **(Optional) Add HTTPS with Certbot once HTTP is working.**



..
  todo::

.. 
    Fix padding on code boxes.
        Furo was already adding padding...removed padding from .highlight in style.css