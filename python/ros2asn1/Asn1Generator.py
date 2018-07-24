# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import string

class Asn1Generator(object):
    '''
    Class with helper functions to generate ASN.1 (identifiers, comments, etc.)
    '''

    ForbiddenKeywords = [
        "active", "adding", "all", "alternative", "and", "any", "as", "atleast", "axioms", "block", "call", "channel", "comment", "connect", "connection", "constant", "constants", "create", "dcl", "decision", "default", "else", "endalternative", "endblock", "endchannel", "endconnection", "enddecision", "endgenerator", "endmacro", "endnewtype", "endoperator", "endpackage", "endprocedure", "endprocess", "endrefinement", "endselect", "endservice", "endstate", "endsubstructure", "endsyntype", "endsystem", "env", "error", "export", "exported", "external", "fi", "finalized", "for", "fpar", "from", "gate", "generator", "if", "import", "imported", "in", "inherits", "input", "interface", "join", "literal", "literals", "macro", "macrodefinition", "macroid", "map", "mod", "nameclass", "newtype", "nextstate", "nodelay", "noequality", "none", "not", "now", "offspring", "operator", "operators", "or", "ordering", "out", "output", "package", "parent", "priority", "procedure", "process", "provided", "redefined", "referenced", "refinement", "rem", "remote", "reset", "return", "returns", "revealed", "reverse", "save", "select", "self", "sender", "service", "set", "signal", "signallist", "signalroute", "signalset", "spelling", "start", "state", "stop", "struct", "substructure", "synonym", "syntype", "system", "task", "then", "this", "timer", "to", "type", "use", "via", "view", "viewed", "virtual", "with", "xor", "end", "i", "j", "auto", "const",
        # From Nicolas Gillet/Astrium for SCADE
        "abstract", "activate", "and", "assume", "automaton", "bool", "case", "char", "clock", "const", "default", "div", "do", "else", "elsif", "emit", "end", "enum", "every", "false", "fby", "final", "flatten", "fold", "foldi", "foldw", "foldwi", "function", "guarantee", "group", "if", "imported", "initial", "int", "is", "last", "let", "make", "map", "mapfold", "mapi", "mapw", "mapwi", "match", "merge", "mod", "node", "not", "numeric", "of", "onreset", "open", "or", "package", "parameter", "pre", "private", "probe", "public", "real", "restart", "resume", "returns", "reverse", "sensor", "sig", "specialize", "state", "synchro", "tel", "then", "times", "transpose", "true", "type", "unless", "until", "var", "when", "where", "with", "xor",
        # From Maxime - ESA GNC Team
        "open", "close", "flag",
        #From Raquel - ESROCOS
        "name", "size", "data", "range"
    ]

    # Types imported from TASTE-BasicTypes
    ImportsBasic = ['T-Boolean', 'T-Int8', 'T-UInt8', 'T-Int32', 'T-UInt32']

    # Types imported from TASTE-ExtendedTypes
    ImportsExtended = ['T-Int16', 'T-UInt16', 'T-Int64', 'T-UInt64', 'T-Float', 'T-Double', 'T-String', 'T-Time']

    @classmethod
    def asn_package_name(cls, pkgname):
        '''Package name in ASN.1 '''
        return string.replace(pkgname.capitalize() + '-Types', '_', '-')
        
    @classmethod
    def asn_type_name(cls, pkgname, typename):
        '''Transform string to ASN.1 type name'''
        return string.replace(pkgname.capitalize() + '-' + typename, '_', '-')
        
    @classmethod
    def asn_field_name(cls, fieldname):
        '''Transform string to ASN.1 field name'''
        if fieldname.lower() in cls.ForbiddenKeywords:
            fieldname = fieldname + '-value'
        uncap = fieldname[0].lower() + fieldname[1:] if fieldname else ''
        return string.replace(uncap, '_', '-')
        
    @classmethod
    def asn_constant_name(cls, constname):
        '''Transform string to ASN.1 constant name'''
        uncap = constname[0].lower() + constname[1:] if constname else ''
        return string.replace(uncap, '_', '-')
        
    @classmethod
    def asn_comment(cls, txt, indent=1):
        '''Returns a text commentted in ASN.1'''
        outtxt = ''
        for line in txt.splitlines(True):
            outtxt = outtxt + '    '*indent + '-- ' + line
        return outtxt
       
