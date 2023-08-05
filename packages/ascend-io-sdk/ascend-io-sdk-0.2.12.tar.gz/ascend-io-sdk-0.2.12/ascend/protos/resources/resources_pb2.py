# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ascend/protos/resources/resources.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ascend/protos/resources/resources.proto',
  package='resources',
  syntax='proto3',
  serialized_options=b'\n\032io.ascend.protos.resourcesP\001\240\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'ascend/protos/resources/resources.proto\x12\tresources\"\x16\n\x03\x43pu\x12\x0f\n\x07quantum\x18\x01 \x01(\x01\"\x1b\n\x08TaskSets\x12\x0f\n\x07quantum\x18\x01 \x01(\x01\"\x1e\n\x0b\x43ontrolPath\x12\x0f\n\x07quantum\x18\x01 \x01(\x03\"\"\n\x0f\x41ntiControlPath\x12\x0f\n\x07quantum\x18\x01 \x01(\x03\"\xc7\x01\n\x08Resource\x12\x1d\n\x03\x63pu\x18\x01 \x01(\x0b\x32\x0e.resources.CpuH\x00\x12(\n\ttask_sets\x18\x02 \x01(\x0b\x32\x13.resources.TaskSetsH\x00\x12.\n\x0c\x63ontrol_path\x18\x03 \x01(\x0b\x32\x16.resources.ControlPathH\x00\x12\x37\n\x11\x61nti_control_path\x18\x04 \x01(\x0b\x32\x1a.resources.AntiControlPathH\x00\x42\t\n\x07\x64\x65tails\"2\n\tResources\x12%\n\x08resource\x18\x01 \x03(\x0b\x32\x13.resources.ResourceB!\n\x1aio.ascend.protos.resourcesP\x01\xa0\x01\x01\x62\x06proto3'
)




_CPU = _descriptor.Descriptor(
  name='Cpu',
  full_name='resources.Cpu',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='quantum', full_name='resources.Cpu.quantum', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=54,
  serialized_end=76,
)


_TASKSETS = _descriptor.Descriptor(
  name='TaskSets',
  full_name='resources.TaskSets',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='quantum', full_name='resources.TaskSets.quantum', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=78,
  serialized_end=105,
)


_CONTROLPATH = _descriptor.Descriptor(
  name='ControlPath',
  full_name='resources.ControlPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='quantum', full_name='resources.ControlPath.quantum', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=137,
)


_ANTICONTROLPATH = _descriptor.Descriptor(
  name='AntiControlPath',
  full_name='resources.AntiControlPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='quantum', full_name='resources.AntiControlPath.quantum', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=173,
)


_RESOURCE = _descriptor.Descriptor(
  name='Resource',
  full_name='resources.Resource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpu', full_name='resources.Resource.cpu', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_sets', full_name='resources.Resource.task_sets', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='control_path', full_name='resources.Resource.control_path', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='anti_control_path', full_name='resources.Resource.anti_control_path', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='details', full_name='resources.Resource.details',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=176,
  serialized_end=375,
)


_RESOURCES = _descriptor.Descriptor(
  name='Resources',
  full_name='resources.Resources',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource', full_name='resources.Resources.resource', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=377,
  serialized_end=427,
)

_RESOURCE.fields_by_name['cpu'].message_type = _CPU
_RESOURCE.fields_by_name['task_sets'].message_type = _TASKSETS
_RESOURCE.fields_by_name['control_path'].message_type = _CONTROLPATH
_RESOURCE.fields_by_name['anti_control_path'].message_type = _ANTICONTROLPATH
_RESOURCE.oneofs_by_name['details'].fields.append(
  _RESOURCE.fields_by_name['cpu'])
_RESOURCE.fields_by_name['cpu'].containing_oneof = _RESOURCE.oneofs_by_name['details']
_RESOURCE.oneofs_by_name['details'].fields.append(
  _RESOURCE.fields_by_name['task_sets'])
_RESOURCE.fields_by_name['task_sets'].containing_oneof = _RESOURCE.oneofs_by_name['details']
_RESOURCE.oneofs_by_name['details'].fields.append(
  _RESOURCE.fields_by_name['control_path'])
_RESOURCE.fields_by_name['control_path'].containing_oneof = _RESOURCE.oneofs_by_name['details']
_RESOURCE.oneofs_by_name['details'].fields.append(
  _RESOURCE.fields_by_name['anti_control_path'])
_RESOURCE.fields_by_name['anti_control_path'].containing_oneof = _RESOURCE.oneofs_by_name['details']
_RESOURCES.fields_by_name['resource'].message_type = _RESOURCE
DESCRIPTOR.message_types_by_name['Cpu'] = _CPU
DESCRIPTOR.message_types_by_name['TaskSets'] = _TASKSETS
DESCRIPTOR.message_types_by_name['ControlPath'] = _CONTROLPATH
DESCRIPTOR.message_types_by_name['AntiControlPath'] = _ANTICONTROLPATH
DESCRIPTOR.message_types_by_name['Resource'] = _RESOURCE
DESCRIPTOR.message_types_by_name['Resources'] = _RESOURCES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cpu = _reflection.GeneratedProtocolMessageType('Cpu', (_message.Message,), {
  'DESCRIPTOR' : _CPU,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.Cpu)
  })
_sym_db.RegisterMessage(Cpu)

TaskSets = _reflection.GeneratedProtocolMessageType('TaskSets', (_message.Message,), {
  'DESCRIPTOR' : _TASKSETS,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.TaskSets)
  })
_sym_db.RegisterMessage(TaskSets)

ControlPath = _reflection.GeneratedProtocolMessageType('ControlPath', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLPATH,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.ControlPath)
  })
_sym_db.RegisterMessage(ControlPath)

AntiControlPath = _reflection.GeneratedProtocolMessageType('AntiControlPath', (_message.Message,), {
  'DESCRIPTOR' : _ANTICONTROLPATH,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.AntiControlPath)
  })
_sym_db.RegisterMessage(AntiControlPath)

Resource = _reflection.GeneratedProtocolMessageType('Resource', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCE,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.Resource)
  })
_sym_db.RegisterMessage(Resource)

Resources = _reflection.GeneratedProtocolMessageType('Resources', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCES,
  '__module__' : 'ascend.protos.resources.resources_pb2'
  # @@protoc_insertion_point(class_scope:resources.Resources)
  })
_sym_db.RegisterMessage(Resources)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
