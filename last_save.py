import json
import os

LAST_SAVE_FILENAME = '.last_save_gui.json'
LAST_SAVE_DIR_KEY = 'last_save_dir'
DEFAULT_LAST_SAVE_DIR = '.'

class LastSave():
	def __init__(self):
		self.last_save_dir = None
		if os.path.isfile(LAST_SAVE_FILENAME):
			try:
				with open(LAST_SAVE_FILENAME) as f:
					self.last_save_dir = json.loads(f.read()).get(LAST_SAVE_DIR_KEY,'.')
			except Exception as e:
				print(e)

		if self.last_save_dir is None:
			self.last_save_dir = DEFAULT_LAST_SAVE_DIR

		self._update_dir()

	def update_dir(self, new_dir):
		self.last_save_dir = new_dir
		self._update_dir()

	def get_dir(self):
		return self.last_save_dir

	def _update_dir(self):
		if self.last_save_dir is None:
			self.last_save_dir = DEFAULT_LAST_SAVE_DIR

		with open(LAST_SAVE_FILENAME, "w") as f:
			f.write(json.dumps({LAST_SAVE_DIR_KEY: self.last_save_dir}))

