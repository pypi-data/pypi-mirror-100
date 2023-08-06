import json

import requests

from .exceptions.exceptions import IncidentNotExistsException, ProcessingStatusDoesNotExistException


class TopdeskConnector:
	def __init__(self, baseURL: str, authkey: str):
		"""
		Base URL example: https://example.topdesk.com/tas/api/
		"""
		self.authkey = authkey
		self.headers = {
			'Authorization': authkey,
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		}
		self.baseURL = baseURL

	def make_request(self, method, url_extension, params=None, headers=None, files=None, json_data=None, auto_parse=True):
		"""
		Make a request to the API and return the repsonse content

		:param auto_parse: bool: Wether the response should be automatically parsed from json. Disable this for requests like filereponses.
		:param method: [string] HTTP method e.g. "POST", "GET"
		:param url_extension: [string] extension of the base url. e.g. incidents/
		:param params: [dict] parameters to be added to the request
		:param headers: [dict] headers to be added to the request
		:param files: [dict] files to be added to the request
		:param: json_data [dict] Body data.
		:return: [dict] response body
		"""
		url = self.baseURL + url_extension
		# get default headers if not set.
		if headers is None:
			headers = self.headers
		response = requests.request(method, url, params=params, headers=headers, files=files, json=json_data)
		if 200 <= response.status_code <= 299:
			if response.content:
				if auto_parse:
					return json.loads(response.content)
				else:
					return response
			else:
				return ""
		else:
			raise json.JSONDecodeError(response.reason, str(response.content), 22)

	def valid_connection(self):
		"""
		Test de verbinding met Topdesk
		:return: bool
		"""
		response = self.make_request('get', 'version', auto_parse=False)
		if response.status_code == 200:
			return True
		return False

	def incident(self, incident_id: str):
		"""
		Verkrijg een incident op basis van het incident ID
		Args:
			incident_id:

		Returns: Incident

		"""
		params = {'id': f"{incident_id}"}
		incident = self.make_request('get', 'incidents/', params=params)
		if incident:
			return incident[0]
		else:
			raise IncidentNotExistsException()

	def __incidents(self, params: dict = None):
		"""
		Verkrijg een lisjt van incidenten
		Args:
			params: paramters die gebruikt kunnen worden om te sorteren of filteren. https://developers.topdesk.com/documentation/index.html#api-Incident-GetListOfIncidents

		Returns:

		"""
		return self.make_request('get', 'incidents/', params=params)

	# def incidents_grouped_by_calltype(self, page_size: int = 10):
	# 	"""
	# 	Verkrijg een lijst van incidenten gegroepeerd op callType en geordend op prioriteit.
	#
	# 	Args:
	# 		page_size: hoeveelheid incidenten
	#
	# 	Returns: lisjt van incidenten
	# 	"""
	# 	params = {
	# 		"order_by": "target_date",
	# 		"processing_status": "95fcb25f-e1c3-4e89-a90d-81e563117086", # In behandeling
	# 	}
	# 	event_incidents = self.__incidents(params=params)
	# 	return event_incidents

	def incident_status(self, incident_id: str):
		"""
		Return de status string van een incident

		Args:
			incident_id:

		Returns: Status string

		"""
		incident = self.incident(incident_id)
		return incident.get('status')

	def update_incident(self, incident_id: str, modifications: dict):
		"""
		Update een incident.
		Args:
			incident_id: str
			modifications: dictionairy met de gewenste aanpassingen. bijvoorbeeld: {"processingStatus": {"name": "Gereed"}}

		Returns: Incident
		"""
		try:
			return self.make_request("PUT", f'incidents/id/{incident_id}', json_data=modifications, auto_parse=True)
		except json.JSONDecodeError as e:
			# If we get a message saying nothing has changed, just continue. If not, rethrow the error.
			if not e.doc == 'b\'[{"message":"No fields changed"}]\'':
				print(e.doc)
				raise json.JSONDecodeError(e.doc, e.doc, e.pos)
			return self.incident(incident_id=incident_id)

	def incident_status_to_done(self, incident_id: str):
		"""
		Update de processingStatus van een incident naar Gereed.

		Args:
			incident_id: str: Incident id

		Returns: None

		"""
		status = {"processingStatus": {"name": "Gereed"}}
		return self.update_incident(incident_id=incident_id, modifications=status)

	def set_expenses(self, incident_id: str, expenses: float):
		"""
		Update het onkosten veld van een incident.
		Args:
			incident_id: String
			expenses: Float

		Returns: incident.

		"""
		modifications = {'costs': str(expenses)}
		return self.update_incident(incident_id=incident_id, modifications=modifications)

	def incident_add_action(self, incident_id: str, text: str):
		"""
		Add een tekst in het actie veld in topdesk.
		Args:
			incident_id:
			text: Actie tekst die wordt vermeld in topdesk.

		Returns: Incident.
		"""
		modification = {"action": text}
		return self.update_incident(incident_id=incident_id, modifications=modification)

	def incident_actions(self, incident_id: str):
		"""
		Get incident actions op basis van een incident_id.

		Args:
			incident_id: [string]: incident id

		Returns:

		"""
		return self.make_request('get', f'/incidents/id/{incident_id}/actions')

	def incident_call_type(self, incident_id: str):
		"""
		Return de callType string van een incident

		Args:
			incident_id:

		Returns: Status string calltype

		"""
		incident = self.incident(incident_id)
		return incident.get('callType').get('name')

	def incidents_supplier(self, supplier_id, amount=5):
		"""
		Get all incidents linked to a supplier id
		:param amount: amount of incidents to request.
		:param supplier_id: string
		:return:
		"""
		# naam: Comparex Nederland B.V.
		params = {
			'supplier': { "id": f"{supplier_id}" },
			'page_size': amount
		}
		return self.make_request('GET', "incidents", params=params)

	def newest_incidents(self, amount=5, start_offset=0, processing_status_id: str = None):
		"""
		Verkrijg een lijst van incidenten, gesorteerd op nieuw naar oud
				:param
		:return:
		Args:
			amount: [int]: Amount of incidents. Default = 5
			start_offset: [int] Start offset. Begin bij x
			processing_status: [string] Processing status ID. Als None, alle processing statuses

		Returns: [dictionary] - Lijst van incidenten

		"""
		params = {
			"order_by": "creation_date+DESC",
			"page_size": f"{amount}",
			"start": f"{start_offset}",
			"status": "secondLine"
		}
		if processing_status_id:
			params['processing_status'] = processing_status_id
		return self.make_request('get', 'incidents/', params=params)

	def processing_status_id(self, name: str):
		"""
		Verkrijg de processing status id op basis van een naam

		Args:
			name: naam van de processing status

		Returns: string | None: processing status id
		"""
		statuses = self.make_request('get', 'incidents/statuses')
		for status in statuses:
			if status["name"] == name:
				return status['id']
		raise ProcessingStatusDoesNotExistException

	def incident_attachments(self, id, start=0, page_size=10):
		"""
		Get attachments by incident ID
		:param id: incident id
		:param start: index start
		:param page_size: amount of elements per page
		:return: dict: dict of attachments
		"""
		params = {
			'start': start,
			'page_size': page_size
		}
		return self.make_request('GET', f"incidents/id/{id}/attachments")

	def incident_newest_attachment_grouped(self, incident_id: str, filter_list: list = None):
		"""
		Verrkijg incident attachments gegroepeerd in een dictionary op basis van de filter list. Filter list is een
		lijst van labels waar de attachments op worden gesorteerd. Als de filter_list niet wordt meegegeven, worden
		offerte, werkbon en factuur gebruikt als standaard waardes.

		Args:
			incident_id:
			filter_list: een list met labels waar op gezocht wordt. Alleen attachments die de naam van een label bevat
			wordt opgenomen in de dictionary. De items van deze list worden als keys van de dict gebruikt.
		Returns:

		"""
		files = self.incident_attachments(incident_id)
		files_dict = {}
		if filter_list is None:
			filter_list = ['offerte', 'werkbon', 'factuur']
		# Loop achteruit over de file heen, hierdoor worden de meest recente bestanden uiteindelijk gereturned.
		for file in files[::-1]:
			for label in filter_list:
				if label in file.get('fileName'):
					files_dict[label] = file

		return files_dict

	def upload_attachment_to_incident(self, incident_id: int, file_handle):
		"""
		Upload een attachment naar een incident in topdesk.
		:param filename: string incl. extensie
		:param incident_id: int
		:param file_handle: File. Bijvoorbeeld zoals in request.FILES
		:return: response
		"""
		# Custom headers hiervoor om data-type te vermijden
		headers = {
			'Authorization': self.authkey,
			'Accept': 'application/json',
		}
		url = f"incidents/id/{incident_id}/attachments"
		params = {
			"invisibleForCaller": False,
		}
		files = {'file': file_handle}
		return self.make_request('post', url, params=params, files=files, headers=headers)

	def download_attachment(self, incident_id, attachment_id):
		"""
		Download a given attachment

		:param incident_id:
		:param attachment_id:

		:return: tuple: (content, filename)

		"""
		attachments = self.incident_attachments(incident_id)
		# Get attachment again to find original filename. This is not passed by the client because ideally this is stateless.
		filename = None
		for attachment in attachments:
			if attachment.get('id') == attachment_id:
				filename = attachment.get('fileName')
				break
		if filename is None:
			raise FileNotFoundError("Attachment is niet gevonden tussen de lijst van attachments bij het downloaden. topdesk.py -> download_attachment()")
		response = self.make_request("GET", f"incidents/id/{incident_id}/attachments/{attachment_id}/download", auto_parse=False)
		return response.content, filename

	def create_incident(self, request: str, short_description: str, action: str, status="secondLine", costs: int = 0):
		url = "https://topdesktest.sudwestfryslan.nl/tas/api/incidents"
		body = {
			"request": f"{request}",
			"action": f"{action}",
			"status": f"{status}",
			"caller": {"dynamicName": "Enigma UP"},
			"briefDescription": f"{short_description}",
			"operatorGroup": {
				"id": "5a13f81e-7628-4fe5-9a9f-e3aecfb69579" 	# SWF-Vastgoed, Gebouwenbeheer
			},
			"operator": {
				"id": "c9e896ff-6423-4d3b-934c-e5bcdc92e244"	# Andre duinstra
			},
			"callType": {
				"name": "storing"
			},
			"entryType": {
				"name": "Monitoring"
			},
			"category": {
				"id": "2dffd830-c201-4f03-8138-09757a58eee6"
			},
			"subcategory": {
				"id": "717c3e08-f4b8-4aaa-b4b9-b36bc05254ec"
			},
			"impact": {
				"id": "13859c59-c540-405a-89b2-a43ecfd6c244"
			},
			"urgency": {
				"id": "244c005f-f619-568b-bc7b-bd4ab4ba993a"
			},
			"priority": {
				"id": "d2799bdf-3346-4de2-b0ea-1d0b54c77d1a"
			},
			'costs': f"{costs}"
		}
		response = requests.post(url, json=body, headers=self.headers)
		json_data = json.loads(response.content)
		return json_data

	def operators(self):
		"""
		Get all operators
		:return: [dict]: operators
		"""
		return self.make_request('get', 'operators/')

	def operators_as_tuples(self):
		"""
		Get all operators as a list of tuples. This is mainly used in the user model to link a user to an operator.
		:return: [list]: list of tuples containing ('operatorName', 'operatorId')
		"""
		operators = self.make_request('get', 'operators/', params={'page_size': 100})
		return [(operator.get('id'), operator.get('dynamicName')) for operator in operators]

	def suppliers(self):
		"""
		Get all supplier contacts
		:return: dict
		"""
		return self.make_request('GET', 'suppliers/')

	def suppliers_as_tuples(self):
		"""
		Get all supplier contacts as a list of tuples
		:return: dict
		"""
		suppliers = self.make_request('GET', 'suppliers/')
		return [(supplier.get('id'), supplier.get('name')) for supplier in suppliers]

	# **************************
	# Operations management ****
	# **************************

	def operational_activities(self, ammount: int = 5) -> dict:
		"""
		Verkrijg een lijst van alle operationele activiteiten
		Params:
			ammount: hoeveelheid activiteiten om op te vragen.
		Returns: Dict

		"""
		params = {
			'pageSize': ammount
		}
		return self.make_request('get', 'operationalActivities', params=params).get('result')

	def operational_activity(self, activity_id: str) -> dict:
		"""
		Verkrijg informatie over 1 operational activity

		Args:
			activity_id:

		Returns: dict

		"""
		return self.make_request('get', f'operationalActivities/{activity_id}/')

	# **************************
	# **** Asset management ****
	# **************************

	def asset_upload(self, file, asset_id):
		"""
		Upload een file naar een asset
		Args:
			file: File
			asset_id: string

		Returns:
		"""
		headers = {
			'Authorization': self.authkey,
			'Accept': 'application/json',
		}
		params = {
			'assetId': asset_id
		}
		files = {'file': file}
		return self.make_request('POST', 'assetmgmt/uploads', headers=headers, params=params, files=files)

	def assets_as_tuples(self):
		"""
		Get all assets as a tuple of id and name
		:return: list[tuple()]
		"""
		assets = self.make_request('GET', 'assetmgmt/assets/')
		return [(asset.get('id'), asset.get('text')) for asset in assets.get('dataSet')]
