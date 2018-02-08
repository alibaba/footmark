# footmark
python sdk for aliyun, and give ansible-module used first

## Install footmark
footmark can be intalled conveniently via pip:

	$ sudo pip install footmark
and it can be upgrade via following command:

    $ sudo pip install footmark --upgrade

## Config footmark
By default we use two locations for the footmark configurations, which '/etc/footmark/' and '~/.footmark'. And location '~/.footmark' works on Windows and Unix.
All of footmark's configurations files exist in the locations, and you can configure your footmark by modifying them. At present, footmark only support custom logging.
Footmark logs exist in the '/var/log/footmark', and it only retains the logs last 7 days.

## Unittest footmark
If you want to test footmark use unittest, you should use following command to install dependence packages:

	$ sudo pip install mock nose nose_htmloutput importlib
Warning: If you run it in the Mac, it will failed and raise an error 'OSError: [Errno 1] Operation not permitted:'. The best way to solve it is run it in the virtualenv.

## Package footmark
When you modify footmark, you need to package and distribute it. First, you need to edit footmark/__init__.py and set a new version to '__version__ '. Second execute command as follows:

    # build footmark package
    $ python setup.py sdist

    # make sure your enviroment has installed twine, if not, execute command:
    $ sudo pip install twine

    # distribute new footmark
    # upload your project
	$ twine upload dist/<your-footmark-package>
Finally, upgrade footmark and check it.