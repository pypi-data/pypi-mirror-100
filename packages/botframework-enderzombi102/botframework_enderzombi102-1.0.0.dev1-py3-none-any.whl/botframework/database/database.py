from typing import Dict, Any, List, Tuple

from botframework.abc.database.backend import AbstractBackend
from botframework.abc.database.database import AbstractDatabase
from botframework.database.backend import SqlBackend
from botframework.database.guild import Guild


_tables: Dict[str, List[str] ] = {
	'users': [
		'guildID',
		'discordID',
		'prefix'
	]
}


class Database(AbstractDatabase):

	_cache: Dict[int, Guild] = {}
	instance: 'Database'
	backend: AbstractBackend = None

	def __init__( self ):
		self.backend = SqlBackend('../resources/database.db')
		Database.instance = self

	def getGuild( self, guild: int ) -> Guild:
		"""
		Returns a Guild object for interacting with the database
		:param guild: guid ID
		:return: the Guild Object
		"""
		if guild not in self._cache.keys():
			self._cache[guild] = Guild(guild, self)
		return self._cache.get(guild)

	def makeRequest( self, sql: str, *args, table: str = '' ) -> List[ Dict[str, Any] ]:
		"""
		Makes a request with SQL code to the database.
		DO NOT USE VARIABLES IN THE SQL CODE!
		IS **VERY** INSECURE AND CAN CAUSE DATA LOSS!
		:param table: the table this request operates on
		:param sql: SQL code
		:param args: arguments for value sanitizing
		:return: a List with the result (can be emtpy)
		"""
		return _makeDictionary( table, self.backend.makeRequest(sql, *args) )

	def save( self ) -> None:
		"""	Commit changes to the database file	"""
		if self.backend is not None:
			self.backend.save()

	def __del__( self ):
		# save when closing!
		self.save()


def _makeDictionary( table: str, row: List[Tuple] ) -> List[ Dict[str, Any] ]:
	items: List[ Dict[str, Any] ] = []
	for item in row:
		if table in _tables.keys():
			template = _tables[table]  # get the dictionary template from the known tables
			items.append(
				{
					# associate a key with a value
					template[pos]: value for pos, value in enumerate(item)
				}
			)
		else:
			items.append( { pos: value for pos, value in enumerate(item) } )

	return items
