##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

import yaml
import os
try:
    import simplejson as json
except ImportError:
    import json


class FileStorageError(Exception):
    pass


class BaseFile(object):
    db = None

    def set(self, db):
        if type(db) is not dict:
            raise Exception("You can only set db as a dict, not {}".type(db))
        self.db = db

    def getFileSize(self, fname):
        return os.path.getsize(fname)


class FileJson(BaseFile):
    def read(self, fname):
        """
        Reads a Json file
        in: file name
        out: length of file, dictionary
        """
        try:
            with open(fname, 'r') as f:
                data = json.load(f)

            self.db = data

        except IOError:
            # print '[-] YamlDoc: IOError'
            raise FileStorageError('Could not open {0!s} for reading'.format((fname)))
        except json.errors.JSONDecodeError as e:
            print(e)
            raise

        return self.db

    def write(self, fname, data=None):
        """
        Writes a Json file
        """
        try:
            if data is None:
                data = self.db

            with open(fname, 'w') as f:
                json.dump(data, f)

        except IOError:
            # print '[-] YamlDoc: IOError'
            raise FileStorageError('Could not open {0!s} for writing'.format((fname)))


class FileYaml(BaseFile):
    def read(self, fname):
        """
        Reads a Yaml file
        in: file name
        out: length of file, dictionary
        """
        try:
            f = open(fname, 'r')
            d = yaml.safe_load(f)
            f.close()
            self.db = d

        except IOError:
            # print '[-] YamlDoc: IOError'
            raise FileStorageError('Could not open {0!s} for reading'.format((fname)))

        return self.db

    def write(self, filename, data=None):
        """
        Writes a Yaml file
        in:
            filename - file name
            data - [optional] data to be written, otherwise, it uses data in self.db
        """
        try:
            if data is None:
                data = self.db
            f = open(filename, 'w')
            yaml.safe_dump(data, f)
            f.close()
        except IOError:
            # print '[-] YamlDoc: IOError'
            raise FileStorageError('Could not open {0!s} for writing'.format((filename)))


#
# class FileStorage(object):
#     """
#     Store your API keys or other params in a json/yaml file and then import them
#     with this class. You can also pass a dictionary to this and create a json/yaml
#     file storage. All key/value pairs are stored in a dictionary called db.
#     """
#     db = None
#
#     def readYaml(self, fname):
#         """
#         Reads a Yaml file
#         in: file name
#         out: length of file, dictionary
#         """
#         try:
#             f = open(fname, 'r')
#             d = yaml.safe_load(f)
#             f.close()
#             self.db = d
#             return len(self.db), d
#         except IOError:
#             # print '[-] YamlDoc: IOError'
#             raise FileStorageError('Could not open {0!s} for reading'.format((fname)))
#
#     def writeYaml(self, filename, data=None):
#         """
#         Writes a Yaml file
#         in:
#             filename - file name
#             data - [optional] data to be written, otherwise, it uses data in self.db
#         """
#         try:
#             if data is None:
#                 data = self.db
#             f = open(filename, 'w')
#             yaml.safe_dump(data, f)
#             f.close()
#         except IOError:
#             # print '[-] YamlDoc: IOError'
#             raise FileStorageError('Could not open {0!s} for writing'.format((filename)))
#
#     def readJson(self, fname):
#         """
#         Reads a Json file
#         in: file name
#         out: length of file, dictionary
#         """
#         try:
#             with open(fname, 'r') as f:
#                 data = json.load(f)
#
#             self.db = data
#             return len(self.db), data
#         except IOError:
#             # print '[-] YamlDoc: IOError'
#             raise FileStorageError('Could not open {0!s} for reading'.format((fname)))
#
#     def writeJson(self, fname, data=None):
#         """
#         Writes a Json file
#         """
#         try:
#             if data is None:
#                 data = self.db
#
#             with open(fname, 'w') as f:
#                 json.dump(data, f)
#
#         except IOError:
#             # print '[-] YamlDoc: IOError'
#             raise FileStorageError('Could not open {0!s} for writing'.format((fname)))
#
#     def getKey(self, keyName):
#         """
#         Given a key, returns a value
#         in: key
#         out: value or None
#         """
#         if keyName in self.db: return self.db[keyName]
#         else: return None
#
#     def clear(self):
#         self.db = None
