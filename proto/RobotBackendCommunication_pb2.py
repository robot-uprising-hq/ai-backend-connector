# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/RobotBackendCommunication.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/RobotBackendCommunication.proto',
  package='robotbackendcommunication',
  syntax='proto3',
  serialized_pb=_b('\n%proto/RobotBackendCommunication.proto\x12\x19robotbackendcommunication\"\x1b\n\nScreenshot\x12\r\n\x05image\x18\x01 \x01(\x0c\"\x1d\n\x0b\x41gentAction\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\x05\x32x\n\x18RobotBackendCommunicator\x12\\\n\tGetAction\x12%.robotbackendcommunication.Screenshot\x1a&.robotbackendcommunication.AgentAction\"\x00\x62\x06proto3')
)




_SCREENSHOT = _descriptor.Descriptor(
  name='Screenshot',
  full_name='robotbackendcommunication.Screenshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='robotbackendcommunication.Screenshot.image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=95,
)


_AGENTACTION = _descriptor.Descriptor(
  name='AgentAction',
  full_name='robotbackendcommunication.AgentAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='robotbackendcommunication.AgentAction.action', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=97,
  serialized_end=126,
)

DESCRIPTOR.message_types_by_name['Screenshot'] = _SCREENSHOT
DESCRIPTOR.message_types_by_name['AgentAction'] = _AGENTACTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Screenshot = _reflection.GeneratedProtocolMessageType('Screenshot', (_message.Message,), dict(
  DESCRIPTOR = _SCREENSHOT,
  __module__ = 'proto.RobotBackendCommunication_pb2'
  # @@protoc_insertion_point(class_scope:robotbackendcommunication.Screenshot)
  ))
_sym_db.RegisterMessage(Screenshot)

AgentAction = _reflection.GeneratedProtocolMessageType('AgentAction', (_message.Message,), dict(
  DESCRIPTOR = _AGENTACTION,
  __module__ = 'proto.RobotBackendCommunication_pb2'
  # @@protoc_insertion_point(class_scope:robotbackendcommunication.AgentAction)
  ))
_sym_db.RegisterMessage(AgentAction)



_ROBOTBACKENDCOMMUNICATOR = _descriptor.ServiceDescriptor(
  name='RobotBackendCommunicator',
  full_name='robotbackendcommunication.RobotBackendCommunicator',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=128,
  serialized_end=248,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAction',
    full_name='robotbackendcommunication.RobotBackendCommunicator.GetAction',
    index=0,
    containing_service=None,
    input_type=_SCREENSHOT,
    output_type=_AGENTACTION,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ROBOTBACKENDCOMMUNICATOR)

DESCRIPTOR.services_by_name['RobotBackendCommunicator'] = _ROBOTBACKENDCOMMUNICATOR

# @@protoc_insertion_point(module_scope)