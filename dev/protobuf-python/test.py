#!/usr/bin/env python2
# https://developers.airmap.com/v2.0/docs/sending-telemetry
from __future__ import print_function
import address_pb2 as addressbook_pb2

person = addressbook_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.HOME

print(person.SerializeToString())
print(phone)
