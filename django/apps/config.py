MODELS_MODULE_NAME = 'models'


class AppConfig:
	""" Class representing a Django application and its configuration."""

	def __init__(self, app_name, app_module):
		# Full python path to the application e.g. 'django.contrib.admin'
		self.name = app_name

		# Root module for the application e.g. <module 'django.contrib.admin'
		# from 'django/contrib/admin/__init__.py'>.
		self.module = app_module

		# Reference to the Apps registry that holds this AppConfig. Set by the
		# registry when it registers the AppConfig instance.
		self.apps = None

		# The following attributes coule be defined at the class level in a
		# subclass, hence the test-and-set pattern.

		# Last component of the Python path to the application e.g. 'admin'.
		# This value must be unique across a Django project.
		if not hasattr(self, 'label'):
			self.label = app_name.rpartition(".")[2]

		# Human-readable name for the application e.g. 'Admin'.
		if not hasattr(self, 'verbose_name'):
			self.verbose_name = self.label.title()

		# Filesystem path to the application directory e.g.
		# '/path/to/django/contrib/admin'.
		if not hasattr(self, 'path'):
			self.path = self._path_from_module(app_module)

		# Module containing models e.g. <module 'django.contrib.admin.models'
		# from 'django/contrib/admin/models.py'>. Set by import_models().
		# None if the application doesn't have a models module.
		self.models_module = None

		# Mapping of lower case model names to model classes. Initially set to
		# None to prevent accidental access before import _models() runs.
		self.models = None

	def __repr__(self):
		return '<%s: %s>' % (self.__class__.__name__, self.label)

	def _path_from_module(self, module):
		"""Attempt to determine app's filesystem from its module."""
		# See #21874 for extended discussion of the behavior of this method in
		# various cases.
		# Convert paths to list because Python's _NamespacePath doesn't support
		# indexing.
		paths = list(getattr(module, '__path__', []))
		if len(paths) != 1:
			filename = getattr(module, '__file__', None)
			if filename is not None:
				paths = [os.path.dirname(filename)]
			else:
				# For unknown reasons, sometimes the list returned by __path__
				# contains duplicates that must be removed (#25246).
				paths = list(set(paths))
			if len(paths) > 1:
				raise ImproperlyConfigured(
					"The app module %r has multiple filesystem locations (%r); "
					"you must configure this app with an AppConfig subclass "
					"with a 'path' class attribute." % (module, paths))
			elif not paths:
				raise ImproperlyConfigured(
					"The app module %r has no filesystem location, "
					"you must configure this app with an Application subclass "
					"with a 'path' class attribute." % (module,))
			return paths[0]
					)
