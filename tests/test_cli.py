# import csv
# import sys
# import json
# import tests
# try:
#     from cStringIO import StringIO
# except ImportError:
#     from io import StringIO
# from six import with_metaclass
# from elex.cli.app import ElexApp
# from collections import OrderedDict

# DATA_FILE = 'tests/data/20151103_national.json'
# DATA_ELECTION_DATE = '2015-11-03'
# DELSUM_DATA_FILE = 'tests/data/20160118_delsum.json'
# DELSUPER_DATA_FILE = 'tests/data/20160118_delsuper.json'
# ELECTIONS_DATA_FILE = 'tests/data/00000000_elections.json'
# DISTRICT_DATA_FILE = 'tests/data/20160201_district_results.json'

# TEST_COMMANDS = [
#     'races',
#     'candidates',
#     'reporting-units',
#     'candidate-reporting-units',
#     'results',
# ]


# class ElexCLICSVTestMeta(type):
#     def __new__(mcs, name, bases, dict):
#         def gen_fields_test(command):
#             """
#             Dynamically generate a fields test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 api_fields = api_data[0].serialize().keys()
#                 self.assertEqual(cli_fields, list(api_fields))
#             return test

#         def gen_length_test(command):
#             """
#             Dynamically generate a data length test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 self.assertEqual(len(cli_data), len(api_data))
#             return test

#         def gen_data_test(command):
#             """
#             Dynamically generate a data test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 for i, row in enumerate(cli_data):
#                     for k, v in api_data[i].serialize().items():
#                         if v is None:
#                             v = ''
#                         self.assertEqual(row[k], str(v))
#             return test

#         def gen_timestamp_test(command):
#             """
#             Generate test to ensure timestamp field is set
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           with_timestamp=True)
#                 self.assertEqual(cli_fields[-1], 'timestamp')

#             return test

#         def gen_timestamp_data_test(command):
#             """
#             Generate test to ensure timestamp field is set
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           with_timestamp=True)
#                 for row in cli_data:
#                     try:
#                         self.assertTrue(unicode(row['timestamp']).isnumeric())
#                     except NameError:
#                         self.assertTrue(str(row['timestamp']).isnumeric())

#             return test

#         def gen_batch_name_data_test(command):
#             """
#             Generate test to ensure timestamp field is set
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           batch_name='batch-01')
#                 for row in cli_data:
#                     self.assertEqual(row['batchname'], 'batch-01')

#             return test

#         for command in TEST_COMMANDS:
#             fields_test_name = 'test_csv_{0}_fields'.format(
#                 command.replace('-', '_')
#             )
#             dict[fields_test_name] = gen_fields_test(command)

#             length_test_name = 'test_csv_{0}_length'.format(
#                 command.replace('-', '_')
#             )
#             dict[length_test_name] = gen_length_test(command)

#             data_test_name = 'test_csv_{0}_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[data_test_name] = gen_data_test(command)

#             timestamp_test_name = 'test_csv_{0}_timestamp'.format(
#                 command.replace('-', '_')
#             )
#             dict[timestamp_test_name] = gen_timestamp_test(command)

#             timestamp_data_test_name = 'test_csv_{0}_timestamp_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[timestamp_data_test_name] = gen_timestamp_data_test(command)

#             batch_name_data_test_name = 'test_csv_{0}_batch_name_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[batch_name_data_test_name] = gen_batch_name_data_test(command)

#         return type.__new__(mcs, name, bases, dict)


# class ElexCLICSVTestCase(
#     with_metaclass(ElexCLICSVTestMeta, tests.ElectionResultsTestCase)
# ):
#     """
#     This testing class is mostly dynamically generated by its metaclass.

#     The goal of the CLI tests is to the make sure the CLI output matches the
#     Python API. The API tests guarantee the validity of the data, while these
#     tests guarantee the CLI provides the same data in CSV format.
#     """
#     def test_csv_elections_fields(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(
#             fields,
#             ['id', 'electiondate', 'liveresults', 'testresults']
#         )

#     def test_csv_elections_length(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(len(data), 11)

#     def test_csv_elections_date(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['electiondate'], '2015-08-04')

#     def test_csv_elections_liveresults(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['liveresults'], 'False')

#     def test_csv_elections_testresults(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['testresults'], 'True')

#     def test_csv_next_election_fields(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(
#             fields,
#             ['id', 'electiondate', 'liveresults', 'testresults']
#         )

#     def test_csv_next_election_length(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(len(data), 1)

#     def test_csv_next_election_date(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['electiondate'], '2015-08-25')

#     def test_csv_next_election_liveresults(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['liveresults'], 'True')

#     def test_csv_next_election_testresults(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['testresults'], 'False')

#     def test_csv_delegate_fields(self):
#         fields, data = self._test_command(command='delegates')
#         self.assertEqual(
#             fields,
#             [
#                 'level', 'party_total', 'superdelegates_count', 'last',
#                 'state', 'candidateid', 'party_need', 'party',
#                 'delegates_count', 'id', 'd1', 'd7', 'd30'
#             ]
#         )

#     def test_csv_delegate_state_count(self):
#         fields, data = self._test_command(command='delegates')
#         number_of_states = list(
#             set([d['state'] for d in data if d['level'] == 'state'])
#         )
#         self.assertEqual(58, len(number_of_states))

#     def test_csv_results_resultslevel(self):
#         fields, data = self._test_command(
#             command='results',
#             datafile=DISTRICT_DATA_FILE,
#             resultslevel='district'
#         )
#         self.assertEqual(data[17]['reportingunitname'], 'District 1')

#     def _test_command(
#         self,
#         command,
#         datafile=DATA_FILE,
#         delsum_datafile=DELSUM_DATA_FILE,
#         delsuper_datafile=DELSUPER_DATA_FILE,
#         electiondate=DATA_ELECTION_DATE,
#         resultslevel=None,
#         with_timestamp=False,
#         batch_name=False
#     ):
#         """
#         Execute an `elex` sub-command; returns fieldnames and rows
#         """
#         stdout_backup = sys.stdout
#         sys.stdout = StringIO()

#         argv = [command]

#         if electiondate is not None:
#             argv.append(electiondate)

#         argv = argv + ['--data-file', datafile]
#         argv = argv + ['--delegate-sum-file', delsum_datafile]
#         argv = argv + ['--delegate-super-file', delsuper_datafile]
#         argv = argv + ['--results-level', resultslevel]

#         if with_timestamp:
#             argv = argv + ['--with-timestamp']

#         if batch_name:
#             argv = argv + ['--batch-name', batch_name]

#         app = ElexApp(argv=argv)

#         app.setup()
#         app.log.set_level('FATAL')
#         app.run()

#         lines = sys.stdout.getvalue().split('\n')
#         reader = csv.DictReader(lines)

#         sys.stdout.close()
#         sys.stdout = stdout_backup

#         return reader.fieldnames, list(reader)


# class ElexCLIJSONTestMeta(type):
#     def __new__(mcs, name, bases, dict):
#         def gen_fields_test(command):
#             """
#             Dynamically generate a fields test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 api_fields = api_data[0].serialize().keys()
#                 self.assertEqual(cli_fields, list(api_fields))
#             return test

#         def gen_length_test(command):
#             """
#             Dynamically generate a data length test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 self.assertEqual(len(cli_data), len(api_data))
#             return test

#         def gen_data_test(command):
#             """
#             Dynamically generate a data test
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command)
#                 api_data = getattr(self, command.replace('-', '_'))
#                 for i, row in enumerate(cli_data):
#                     for k, v in api_data[i].serialize().items():
#                         self.assertEqual(row[k], v)
#             return test

#         def gen_timestamp_test(command):
#             """
#             Generate test to ensure timestamp field is set
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           with_timestamp=True)
#                 self.assertEqual(cli_fields[-1], 'timestamp')

#             return test

#         def gen_timestamp_data_test(command):
#             """
#             Generate test to ensure timestamp data is an integer
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           with_timestamp=True)
#                 for row in cli_data:
#                     try:
#                         self.assertTrue(unicode(row['timestamp']).isnumeric())
#                     except NameError:
#                         self.assertTrue(str(row['timestamp']).isnumeric())

#             return test

#         def gen_batch_name_data_test(command):
#             """
#             Generate test to ensure timestamp field is set
#             """
#             def test(self):
#                 cli_fields, cli_data = self._test_command(command=command,
#                                                           batch_name='batch-01')
#                 for row in cli_data:
#                     self.assertEqual(row['batchname'], 'batch-01')

#             return test

#         for command in TEST_COMMANDS:
#             fields_test_name = 'test_json_{0}_fields'.format(
#                 command.replace('-', '_')
#             )
#             dict[fields_test_name] = gen_fields_test(command)

#             length_test_name = 'test_json_{0}_length'.format(
#                 command.replace('-', '_')
#             )
#             dict[length_test_name] = gen_length_test(command)

#             data_test_name = 'test_json_{0}_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[data_test_name] = gen_data_test(command)

#             timestamp_data_test_name = 'test_json_{0}_data_timestamp'.format(
#                 command.replace('-', '_')
#             )
#             dict[timestamp_data_test_name] = gen_timestamp_test(command)

#             timestamp_data_test_name = 'test_json_{0}_timestamp_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[timestamp_data_test_name] = gen_timestamp_data_test(command)

#             batch_name_data_test_name = 'test_csv_{0}_batch_name_data'.format(
#                 command.replace('-', '_')
#             )
#             dict[batch_name_data_test_name] = gen_batch_name_data_test(command)

#         return type.__new__(mcs, name, bases, dict)


# class ElexCLIJSONTestCase(
#     with_metaclass(ElexCLIJSONTestMeta, tests.ElectionResultsTestCase)
# ):
#     """
#     This testing class is mostly dynamically generated by its metaclass.

#     The goal of the CLI tests is to the make sure the CLI output matches the
#     Python API. The API tests guarantee the validity of the data, while these
#     tests guarantee the CLI provides the same data in JSON format.
#     """
#     def test_json_elections_fields(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(
#             fields,
#             ['id', 'electiondate', 'liveresults', 'testresults']
#         )

#     def test_json_elections_length(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(len(data), 11)

#     def test_json_elections_date(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['electiondate'], '2015-08-04')

#     def test_json_elections_liveresults(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['liveresults'], False)

#     def test_json_elections_testresults(self):
#         fields, data = self._test_command(
#             command='elections',
#             datafile=ELECTIONS_DATA_FILE
#         )
#         self.assertEqual(data[4]['testresults'], True)

#     def test_json_next_election_fields(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(
#             fields,
#             ['id', 'electiondate', 'liveresults', 'testresults']
#         )

#     def test_json_next_election_length(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(len(data), 1)

#     def test_json_next_election_date(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['electiondate'], '2015-08-25')

#     def test_json_next_election_liveresults(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['liveresults'], True)

#     def test_json_next_election_testresults(self):
#         fields, data = self._test_command(
#             command='next-election',
#             datafile=ELECTIONS_DATA_FILE,
#             electiondate='2015-08-04'
#         )
#         self.assertEqual(data[0]['testresults'], False)

#     def test_json_delegate_fields(self):
#         fields, data = self._test_command(command='delegates')
#         self.assertEqual(
#             fields,
#             [
#                 'level', 'party_total', 'superdelegates_count', 'last',
#                 'state', 'candidateid', 'party_need', 'party',
#                 'delegates_count', 'id', 'd1', 'd7', 'd30'
#             ]
#         )

#     def test_json_delegate_state_count(self):
#         fields, data = self._test_command(command='delegates')
#         number_of_states = list(
#             set([d['state'] for d in data if d['level'] == 'state'])
#         )
#         self.assertEqual(58, len(number_of_states))

#     def test_json_results_resultslevel(self):
#         fields, data = self._test_command(
#             command='results',
#             datafile=DISTRICT_DATA_FILE,
#             resultslevel='district'
#         )
#         self.assertEqual(data[17]['reportingunitname'], 'District 1')

#     def _test_command(
#         self,
#         command,
#         datafile=DATA_FILE,
#         delsum_datafile=DELSUM_DATA_FILE,
#         delsuper_datafile=DELSUPER_DATA_FILE,
#         electiondate=DATA_ELECTION_DATE,
#         resultslevel=None,
#         with_timestamp=False,
#         batch_name=False
#     ):
#         """
#         Execute an `elex` sub-command; returns fieldnames and rows
#         """
#         stdout_backup = sys.stdout
#         sys.stdout = StringIO()

#         argv = [command]

#         argv.append(electiondate)

#         argv = argv + ['--data-file', datafile, '-o', 'json']
#         argv = argv + ['--delegate-sum-file', delsum_datafile]
#         argv = argv + ['--delegate-super-file', delsuper_datafile]
#         argv = argv + ['--results-level', resultslevel]

#         if with_timestamp:
#             argv = argv + ['--with-timestamp']

#         if batch_name:
#             argv = argv + ['--batch-name', batch_name]

#         app = ElexApp(argv=argv)

#         app.setup()
#         app.log.set_level('FATAL')
#         app.run()

#         json_data = sys.stdout.getvalue()
#         data = json.loads(json_data, object_pairs_hook=OrderedDict)

#         sys.stdout.close()
#         sys.stdout = stdout_backup

#         return list(data[0].keys()), data
