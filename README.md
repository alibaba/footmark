# footmark
python sdk for aliyun, used by ansible-module primarily.

## Install footmark
footmark can be intalled via pip:

	$ sudo pip install footmark
and it can be upgraded via the following command:

    $ sudo pip install footmark --upgrade

## Config footmark
By default we use two locations for the footmark configurations, which '/etc/footmark/' and '~/.footmark'. And location '~/.footmark' works on Windows and Unix.
All of footmark's configuration files exist in the locations, and you can configure your footmark by modifying them. At present, footmark only supports custom logging.
Footmark logs exist in '/var/log/footmark', and it only retains the logs for the last 7 days.

## Unittest footmark
If you want to test footmark use unittest, you should use the following command to install dependency packages:

	$ sudo pip install mock nose nose_htmloutput importlib
Warning: If you run it in the Mac, it will fail and raise an error 'OSError: [Errno 1] Operation not permitted:'. To solve the problem, please run it in the virtualenv.

## Package footmark
When you modify footmark, you need to package and distribute it. First, you need to edit footmark/__init__.py and set a new version to '__version__ '. Second, execute commands as follows:

    # build footmark package
    $ python setup.py sdist

    # make sure your enviroment has installed twine, if not, execute command:
    $ sudo pip install twine

    # distribute new footmark
    # upload your project
	$ twine upload dist/<your-footmark-package>
Finally, upgrade footmark and check it.
