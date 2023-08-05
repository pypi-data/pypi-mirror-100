# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: graph.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='graph.proto',
  package='graph',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bgraph.proto\x12\x05graph\"\x0e\n\x0cNullArgument\"\x1e\n\x0cHealthStatus\x12\x0e\n\x06status\x18\x01 \x01(\t\"\x17\n\x07PNLPath\x12\x0c\n\x04path\x18\x01 \x01(\t\"\x1a\n\nScriptPath\x12\x0c\n\x04path\x18\x01 \x01(\t\"*\n\x12ScriptCompositions\x12\x14\n\x0c\x63ompositions\x18\x01 \x03(\t\"&\n\x10ScriptComponents\x12\x12\n\ncomponents\x18\x01 \x03(\t\"\x19\n\tGraphName\x12\x0c\n\x04name\x18\x01 \x01(\t\"#\n\rParameterList\x12\x12\n\nparameters\x18\x01 \x03(\t\"\x1d\n\rComponentName\x12\x0c\n\x04name\x18\x01 \x01(\t\"3\n\tGraphJSON\x12\x13\n\x0bobjectsJSON\x18\x01 \x01(\t\x12\x11\n\tstyleJSON\x18\x02 \x01(\t\"\x1e\n\tStyleJSON\x12\x11\n\tstyleJSON\x18\x01 \x01(\t\"&\n\x07ndArray\x12\r\n\x05shape\x18\x01 \x03(\r\x12\x0c\n\x04\x64\x61ta\x18\x02 \x03(\x01\"6\n\x06Matrix\x12\x0c\n\x04rows\x18\x01 \x01(\r\x12\x0c\n\x04\x63ols\x18\x02 \x01(\r\x12\x10\n\x04\x64\x61ta\x18\x03 \x03(\x01\x42\x02\x10\x01\"s\n\x05\x45ntry\x12\x15\n\rcomponentName\x18\x01 \x01(\t\x12\x15\n\rparameterName\x18\x02 \x01(\t\x12\x0c\n\x04time\x18\x03 \x01(\t\x12\x0f\n\x07\x63ontext\x18\x04 \x01(\t\x12\x1d\n\x05value\x18\x05 \x01(\x0b\x32\x0e.graph.ndArray\"c\n\tServePref\x12\x15\n\rcomponentName\x18\x01 \x01(\t\x12\x15\n\rparameterName\x18\x02 \x01(\t\x12(\n\tcondition\x18\x03 \x01(\x0e\x32\x15.graph.serveCondition\"4\n\nServePrefs\x12&\n\x0cservePrefSet\x18\x01 \x03(\x0b\x32\x10.graph.ServePref\"\xa6\x01\n\rRunTimeParams\x12\x30\n\x06inputs\x18\x01 \x03(\x0b\x32 .graph.RunTimeParams.InputsEntry\x12%\n\nservePrefs\x18\x02 \x01(\x0b\x32\x11.graph.ServePrefs\x1a<\n\x0bInputsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1c\n\x05value\x18\x02 \x01(\x0b\x32\r.graph.Matrix:\x02\x38\x01*\x92\x01\n\x0eserveCondition\x12\x12\n\x0eINITIALIZATION\x10\x00\x12\x0e\n\nVALIDATION\x10\x01\x12\r\n\tEXECUTION\x10\x02\x12\x0e\n\nPROCESSING\x10\x03\x12\x0c\n\x08LEARNING\x10\x04\x12\x0b\n\x07\x43ONTROL\x10\x05\x12\x0e\n\nSIMULATION\x10\x06\x12\t\n\x05TRIAL\x10\x07\x12\x07\n\x03RUN\x10\x08\x32\xe8\x04\n\nServeGraph\x12\x36\n\rLoadCustomPnl\x12\x0e.graph.PNLPath\x1a\x13.graph.NullArgument\"\x00\x12<\n\nLoadScript\x12\x11.graph.ScriptPath\x1a\x19.graph.ScriptCompositions\"\x00\x12\x35\n\x0cLoadGraphics\x12\x11.graph.ScriptPath\x1a\x10.graph.StyleJSON\"\x00\x12\x45\n\x15GetLoggableParameters\x12\x14.graph.ComponentName\x1a\x14.graph.ParameterList\"\x00\x12\x43\n\x0fGetCompositions\x12\x13.graph.NullArgument\x1a\x19.graph.ScriptCompositions\"\x00\x12<\n\rGetComponents\x12\x10.graph.GraphName\x1a\x17.graph.ScriptComponents\"\x00\x12/\n\x07GetJSON\x12\x10.graph.GraphName\x1a\x10.graph.GraphJSON\"\x00\x12\x39\n\x0bHealthCheck\x12\x13.graph.NullArgument\x1a\x13.graph.HealthStatus\"\x00\x12=\n\x10UpdateStylesheet\x12\x10.graph.StyleJSON\x1a\x13.graph.NullArgument\"\x00(\x01\x12\x38\n\x0eRunComposition\x12\x14.graph.RunTimeParams\x1a\x0c.graph.Entry\"\x00\x30\x01\x62\x06proto3'
)

_SERVECONDITION = _descriptor.EnumDescriptor(
  name='serveCondition',
  full_name='graph.serveCondition',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INITIALIZATION', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='VALIDATION', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXECUTION', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROCESSING', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEARNING', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONTROL', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SIMULATION', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRIAL', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RUN', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=925,
  serialized_end=1071,
)
_sym_db.RegisterEnumDescriptor(_SERVECONDITION)

serveCondition = enum_type_wrapper.EnumTypeWrapper(_SERVECONDITION)
INITIALIZATION = 0
VALIDATION = 1
EXECUTION = 2
PROCESSING = 3
LEARNING = 4
CONTROL = 5
SIMULATION = 6
TRIAL = 7
RUN = 8



_NULLARGUMENT = _descriptor.Descriptor(
  name='NullArgument',
  full_name='graph.NullArgument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=22,
  serialized_end=36,
)


_HEALTHSTATUS = _descriptor.Descriptor(
  name='HealthStatus',
  full_name='graph.HealthStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='graph.HealthStatus.status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=38,
  serialized_end=68,
)


_PNLPATH = _descriptor.Descriptor(
  name='PNLPath',
  full_name='graph.PNLPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='graph.PNLPath.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=70,
  serialized_end=93,
)


_SCRIPTPATH = _descriptor.Descriptor(
  name='ScriptPath',
  full_name='graph.ScriptPath',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='graph.ScriptPath.path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=95,
  serialized_end=121,
)


_SCRIPTCOMPOSITIONS = _descriptor.Descriptor(
  name='ScriptCompositions',
  full_name='graph.ScriptCompositions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='compositions', full_name='graph.ScriptCompositions.compositions', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=123,
  serialized_end=165,
)


_SCRIPTCOMPONENTS = _descriptor.Descriptor(
  name='ScriptComponents',
  full_name='graph.ScriptComponents',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='components', full_name='graph.ScriptComponents.components', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=167,
  serialized_end=205,
)


_GRAPHNAME = _descriptor.Descriptor(
  name='GraphName',
  full_name='graph.GraphName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='graph.GraphName.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=207,
  serialized_end=232,
)


_PARAMETERLIST = _descriptor.Descriptor(
  name='ParameterList',
  full_name='graph.ParameterList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='parameters', full_name='graph.ParameterList.parameters', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=234,
  serialized_end=269,
)


_COMPONENTNAME = _descriptor.Descriptor(
  name='ComponentName',
  full_name='graph.ComponentName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='graph.ComponentName.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=271,
  serialized_end=300,
)


_GRAPHJSON = _descriptor.Descriptor(
  name='GraphJSON',
  full_name='graph.GraphJSON',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='objectsJSON', full_name='graph.GraphJSON.objectsJSON', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='styleJSON', full_name='graph.GraphJSON.styleJSON', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=302,
  serialized_end=353,
)


_STYLEJSON = _descriptor.Descriptor(
  name='StyleJSON',
  full_name='graph.StyleJSON',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='styleJSON', full_name='graph.StyleJSON.styleJSON', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=355,
  serialized_end=385,
)


_NDARRAY = _descriptor.Descriptor(
  name='ndArray',
  full_name='graph.ndArray',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='shape', full_name='graph.ndArray.shape', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='graph.ndArray.data', index=1,
      number=2, type=1, cpp_type=5, label=3,
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
  serialized_start=387,
  serialized_end=425,
)


_MATRIX = _descriptor.Descriptor(
  name='Matrix',
  full_name='graph.Matrix',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rows', full_name='graph.Matrix.rows', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cols', full_name='graph.Matrix.cols', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='graph.Matrix.data', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=427,
  serialized_end=481,
)


_ENTRY = _descriptor.Descriptor(
  name='Entry',
  full_name='graph.Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='componentName', full_name='graph.Entry.componentName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameterName', full_name='graph.Entry.parameterName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='graph.Entry.time', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='context', full_name='graph.Entry.context', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='graph.Entry.value', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  ],
  serialized_start=483,
  serialized_end=598,
)


_SERVEPREF = _descriptor.Descriptor(
  name='ServePref',
  full_name='graph.ServePref',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='componentName', full_name='graph.ServePref.componentName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameterName', full_name='graph.ServePref.parameterName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='condition', full_name='graph.ServePref.condition', index=2,
      number=3, type=14, cpp_type=8, label=1,
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
  serialized_start=600,
  serialized_end=699,
)


_SERVEPREFS = _descriptor.Descriptor(
  name='ServePrefs',
  full_name='graph.ServePrefs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='servePrefSet', full_name='graph.ServePrefs.servePrefSet', index=0,
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
  serialized_start=701,
  serialized_end=753,
)


_RUNTIMEPARAMS_INPUTSENTRY = _descriptor.Descriptor(
  name='InputsEntry',
  full_name='graph.RunTimeParams.InputsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='graph.RunTimeParams.InputsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='graph.RunTimeParams.InputsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=862,
  serialized_end=922,
)

_RUNTIMEPARAMS = _descriptor.Descriptor(
  name='RunTimeParams',
  full_name='graph.RunTimeParams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='inputs', full_name='graph.RunTimeParams.inputs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='servePrefs', full_name='graph.RunTimeParams.servePrefs', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RUNTIMEPARAMS_INPUTSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=756,
  serialized_end=922,
)

_ENTRY.fields_by_name['value'].message_type = _NDARRAY
_SERVEPREF.fields_by_name['condition'].enum_type = _SERVECONDITION
_SERVEPREFS.fields_by_name['servePrefSet'].message_type = _SERVEPREF
_RUNTIMEPARAMS_INPUTSENTRY.fields_by_name['value'].message_type = _MATRIX
_RUNTIMEPARAMS_INPUTSENTRY.containing_type = _RUNTIMEPARAMS
_RUNTIMEPARAMS.fields_by_name['inputs'].message_type = _RUNTIMEPARAMS_INPUTSENTRY
_RUNTIMEPARAMS.fields_by_name['servePrefs'].message_type = _SERVEPREFS
DESCRIPTOR.message_types_by_name['NullArgument'] = _NULLARGUMENT
DESCRIPTOR.message_types_by_name['HealthStatus'] = _HEALTHSTATUS
DESCRIPTOR.message_types_by_name['PNLPath'] = _PNLPATH
DESCRIPTOR.message_types_by_name['ScriptPath'] = _SCRIPTPATH
DESCRIPTOR.message_types_by_name['ScriptCompositions'] = _SCRIPTCOMPOSITIONS
DESCRIPTOR.message_types_by_name['ScriptComponents'] = _SCRIPTCOMPONENTS
DESCRIPTOR.message_types_by_name['GraphName'] = _GRAPHNAME
DESCRIPTOR.message_types_by_name['ParameterList'] = _PARAMETERLIST
DESCRIPTOR.message_types_by_name['ComponentName'] = _COMPONENTNAME
DESCRIPTOR.message_types_by_name['GraphJSON'] = _GRAPHJSON
DESCRIPTOR.message_types_by_name['StyleJSON'] = _STYLEJSON
DESCRIPTOR.message_types_by_name['ndArray'] = _NDARRAY
DESCRIPTOR.message_types_by_name['Matrix'] = _MATRIX
DESCRIPTOR.message_types_by_name['Entry'] = _ENTRY
DESCRIPTOR.message_types_by_name['ServePref'] = _SERVEPREF
DESCRIPTOR.message_types_by_name['ServePrefs'] = _SERVEPREFS
DESCRIPTOR.message_types_by_name['RunTimeParams'] = _RUNTIMEPARAMS
DESCRIPTOR.enum_types_by_name['serveCondition'] = _SERVECONDITION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NullArgument = _reflection.GeneratedProtocolMessageType('NullArgument', (_message.Message,), {
  'DESCRIPTOR' : _NULLARGUMENT,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.NullArgument)
  })
_sym_db.RegisterMessage(NullArgument)

HealthStatus = _reflection.GeneratedProtocolMessageType('HealthStatus', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHSTATUS,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.HealthStatus)
  })
_sym_db.RegisterMessage(HealthStatus)

PNLPath = _reflection.GeneratedProtocolMessageType('PNLPath', (_message.Message,), {
  'DESCRIPTOR' : _PNLPATH,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.PNLPath)
  })
_sym_db.RegisterMessage(PNLPath)

ScriptPath = _reflection.GeneratedProtocolMessageType('ScriptPath', (_message.Message,), {
  'DESCRIPTOR' : _SCRIPTPATH,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ScriptPath)
  })
_sym_db.RegisterMessage(ScriptPath)

ScriptCompositions = _reflection.GeneratedProtocolMessageType('ScriptCompositions', (_message.Message,), {
  'DESCRIPTOR' : _SCRIPTCOMPOSITIONS,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ScriptCompositions)
  })
_sym_db.RegisterMessage(ScriptCompositions)

ScriptComponents = _reflection.GeneratedProtocolMessageType('ScriptComponents', (_message.Message,), {
  'DESCRIPTOR' : _SCRIPTCOMPONENTS,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ScriptComponents)
  })
_sym_db.RegisterMessage(ScriptComponents)

GraphName = _reflection.GeneratedProtocolMessageType('GraphName', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHNAME,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.GraphName)
  })
_sym_db.RegisterMessage(GraphName)

ParameterList = _reflection.GeneratedProtocolMessageType('ParameterList', (_message.Message,), {
  'DESCRIPTOR' : _PARAMETERLIST,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ParameterList)
  })
_sym_db.RegisterMessage(ParameterList)

ComponentName = _reflection.GeneratedProtocolMessageType('ComponentName', (_message.Message,), {
  'DESCRIPTOR' : _COMPONENTNAME,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ComponentName)
  })
_sym_db.RegisterMessage(ComponentName)

GraphJSON = _reflection.GeneratedProtocolMessageType('GraphJSON', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHJSON,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.GraphJSON)
  })
_sym_db.RegisterMessage(GraphJSON)

StyleJSON = _reflection.GeneratedProtocolMessageType('StyleJSON', (_message.Message,), {
  'DESCRIPTOR' : _STYLEJSON,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.StyleJSON)
  })
_sym_db.RegisterMessage(StyleJSON)

ndArray = _reflection.GeneratedProtocolMessageType('ndArray', (_message.Message,), {
  'DESCRIPTOR' : _NDARRAY,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ndArray)
  })
_sym_db.RegisterMessage(ndArray)

Matrix = _reflection.GeneratedProtocolMessageType('Matrix', (_message.Message,), {
  'DESCRIPTOR' : _MATRIX,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.Matrix)
  })
_sym_db.RegisterMessage(Matrix)

Entry = _reflection.GeneratedProtocolMessageType('Entry', (_message.Message,), {
  'DESCRIPTOR' : _ENTRY,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.Entry)
  })
_sym_db.RegisterMessage(Entry)

ServePref = _reflection.GeneratedProtocolMessageType('ServePref', (_message.Message,), {
  'DESCRIPTOR' : _SERVEPREF,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ServePref)
  })
_sym_db.RegisterMessage(ServePref)

ServePrefs = _reflection.GeneratedProtocolMessageType('ServePrefs', (_message.Message,), {
  'DESCRIPTOR' : _SERVEPREFS,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.ServePrefs)
  })
_sym_db.RegisterMessage(ServePrefs)

RunTimeParams = _reflection.GeneratedProtocolMessageType('RunTimeParams', (_message.Message,), {

  'InputsEntry' : _reflection.GeneratedProtocolMessageType('InputsEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMEPARAMS_INPUTSENTRY,
    '__module__' : 'graph_pb2'
    # @@protoc_insertion_point(class_scope:graph.RunTimeParams.InputsEntry)
    })
  ,
  'DESCRIPTOR' : _RUNTIMEPARAMS,
  '__module__' : 'graph_pb2'
  # @@protoc_insertion_point(class_scope:graph.RunTimeParams)
  })
_sym_db.RegisterMessage(RunTimeParams)
_sym_db.RegisterMessage(RunTimeParams.InputsEntry)


_MATRIX.fields_by_name['data']._options = None
_RUNTIMEPARAMS_INPUTSENTRY._options = None

_SERVEGRAPH = _descriptor.ServiceDescriptor(
  name='ServeGraph',
  full_name='graph.ServeGraph',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1074,
  serialized_end=1690,
  methods=[
  _descriptor.MethodDescriptor(
    name='LoadCustomPnl',
    full_name='graph.ServeGraph.LoadCustomPnl',
    index=0,
    containing_service=None,
    input_type=_PNLPATH,
    output_type=_NULLARGUMENT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='LoadScript',
    full_name='graph.ServeGraph.LoadScript',
    index=1,
    containing_service=None,
    input_type=_SCRIPTPATH,
    output_type=_SCRIPTCOMPOSITIONS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='LoadGraphics',
    full_name='graph.ServeGraph.LoadGraphics',
    index=2,
    containing_service=None,
    input_type=_SCRIPTPATH,
    output_type=_STYLEJSON,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetLoggableParameters',
    full_name='graph.ServeGraph.GetLoggableParameters',
    index=3,
    containing_service=None,
    input_type=_COMPONENTNAME,
    output_type=_PARAMETERLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCompositions',
    full_name='graph.ServeGraph.GetCompositions',
    index=4,
    containing_service=None,
    input_type=_NULLARGUMENT,
    output_type=_SCRIPTCOMPOSITIONS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetComponents',
    full_name='graph.ServeGraph.GetComponents',
    index=5,
    containing_service=None,
    input_type=_GRAPHNAME,
    output_type=_SCRIPTCOMPONENTS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetJSON',
    full_name='graph.ServeGraph.GetJSON',
    index=6,
    containing_service=None,
    input_type=_GRAPHNAME,
    output_type=_GRAPHJSON,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='HealthCheck',
    full_name='graph.ServeGraph.HealthCheck',
    index=7,
    containing_service=None,
    input_type=_NULLARGUMENT,
    output_type=_HEALTHSTATUS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateStylesheet',
    full_name='graph.ServeGraph.UpdateStylesheet',
    index=8,
    containing_service=None,
    input_type=_STYLEJSON,
    output_type=_NULLARGUMENT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RunComposition',
    full_name='graph.ServeGraph.RunComposition',
    index=9,
    containing_service=None,
    input_type=_RUNTIMEPARAMS,
    output_type=_ENTRY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVEGRAPH)

DESCRIPTOR.services_by_name['ServeGraph'] = _SERVEGRAPH

# @@protoc_insertion_point(module_scope)
