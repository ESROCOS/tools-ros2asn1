# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

from Asn1Generator import Asn1Generator
import rosmsg
import re
import importlib

class RosAsn1Generator(Asn1Generator):
    '''
    Class to generate the ASN.1 files for a ROS package. Intended for
    passing to Mako templates.
    '''
    
    # Correspondence between ROS primitive types and TASTE Basic and Extended types
    PrimitiveTypes = {
        'bool': 'T-Boolean', 'int8': 'T-Int8', 'uint8': 'T-UInt8',
        'int16': 'T-Int16', 'uint16': 'T-UInt16', 'int32': 'T-Int32',
        'uint32': 'T-UInt32', 'int64': 'T-Int64', 'uint64': 'T-UInt64',
        'float32': 'T-Float', 'float64': 'T-Double', 'string': 'T-String',
        'time': 'T-Time', 'duration': 'T-Time', 'byte': 'T-Int8', 'char': 'T-UInt8'}
        
    BasicTypes = ['T-Boolean', 'T-Int8', 'T-UInt8', 'T-Int32', 'T-UInt32']
    
    # Primitive types that can be represented as OCTET STRING in ASN.1
    OctetTypes = ['uint8', 'byte', 'char']
    
    # Default maximum size for variable size types
    DefaultMaxSize = 60

    def __init__(self, rospack, pkg_name):
        self.rospack = rospack
        self.pkg_name = pkg_name

    def messages(self):
        '''List of names of the messages defined by the package'''
        msgs = rosmsg.list_msgs(self.pkg_name, self.rospack)
        # Remove prefix 'package_name/'
        msgs = [msg.replace(self.pkg_name + '/', '', 1) for msg in msgs]
        return msgs
    
    def package_module(self):
        '''Returns the Python module providing the package's messages (<pkg>.msg)        '''
        modname = self.pkg_name + '.msg'
        module = None
        try:
            module = importlib.import_module(modname)
            return module
        except ImportError as e:
            sys.stderr.write('Couldn\'t load package ' + modname + '\n')

    def message_info(self, msg):
        '''Returns a dictionary with information about a message type'''
        try:
            return self.package_module().__dict__.get(msg).__dict__
        except KeyError:
            sys.stderr.write('Couldn\'t find message ' + msg + '\n')

    def full_text(self, msg):
        '''Returns the full text of the ROS message definition'''
        return self.message_info(msg)['_full_text']
    
    def slot_types(self, msg):
        '''Array of slot types for a message'''
        return self.message_info(msg)['_slot_types']

    def slots(self, msg):
        '''Array of slot names for a message'''
        return self.message_info(msg)['__slots__']
        
    def num_slots(self, msg):
        '''Number of slots in a message'''
        return len(self.slots(msg))
        
    def slot(self, msg, idx):
        '''Name of the nth slot of a message'''
        return self.slots(msg)[idx]

    def slot_type(self, msg, idx):
        '''Type of the nth slot of a message'''
        return self.slot_types(msg)[idx]
        
    def is_scalar(self, msg, idx):
        '''Check if the nth slot of a message is scalar'''
        return re.match('.*\[.*\]', self.slot_type(msg, idx)) == None

    def is_fixed_size(self, msg, idx):
        '''Check if the nth slot of a message is scalar'''
        return re.match('.*\[\b*(\d+)\b*\]', self.slot_type(msg, idx)) != None

    def is_variable_size(self, msg, idx):
        '''Check if the nth slot of a message is scalar'''
        return re.match('.*\[\b*\]', self.slot_type(msg, idx)) != None

    def is_octet_type(self, msg, idx):
        '''Check if a type can be converted to OCTET STRING'''
        typ = self.slot_type(msg, idx)
        return self.get_scalar(typ) in self.OctetTypes and not self.is_scalar(msg, idx)

    def slot_size(self, msg, idx):
        '''Return the size of a fixed size slot; if no fixed size, returns None'''
        match = re.match('.*\[\b*(\d+)\b*\]', self.slot_type(msg, idx))
        if match:
            return match.group(1)
        else:
            return None
    
    def get_scalar(self, typename):
        '''Return the scalar part of a type name'''
        match = re.match('^[^\[]*', typename)
        return match.group(0)
    
    def to_asn_type(self, typename):
        '''Returns the ASN.1 type name corresponding to a slot type'''
        scalar = self.get_scalar(typename)
        if scalar in self.PrimitiveTypes:
            return self.PrimitiveTypes[scalar]
        else:
            match = re.match('(.*)/([^/]*)', scalar)
            if match:
                pkg = match.group(1)
                typ = match.group(2)
                return self.asn_type_name(pkg, typ)
            else:
                return None
                
    def split_type(self, typename):
        '''Split slot type in package, type and size'''
        match = re.match('^(.*)/([^/\[\]]*)(\[.*\])?$', typename)
        if match:
            return match.group(1), match.group(2), match.group(3)
        else:
            return None, None, None
        
    def required_packages(self):
        '''Returns the list of packages needed for all the messages and slots'''
        required = []
        for msg in self.messages():
            for typ in self.slot_types(msg):
                pkg,_,_ = self.split_type(typ)
                if pkg and pkg != self.pkg_name:
                    required.append(pkg)
        return list(set(required))
       
    def required_types(self, pkg):
        '''Returns the list of required types from a package needed for all the messages and slots'''
        required = []
        for msg in self.messages():
            for typ in self.slot_types(msg):
                src,typename,_ = self.split_type(typ)
                if src == pkg:
                    required.append(typename)
        return list(set(required))
        
    def asn_size_constant(self, msg):
        '''Returns the name of the size constant to parametrize a variable size type'''
        return self.asn_constant_name('max-' + self.asn_type_name(self.pkg_name, msg))
        
    def variable_size_messages(self):
        '''Returns the list of messages containing variable-sized slots'''
        result = []
        for msg in self.messages():
            for idx in range(self.num_slots(msg)):
                if self.is_variable_size(msg, idx):
                    result.append(msg)
        return list(set(result))
