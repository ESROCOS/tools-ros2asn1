## H2020 ESROCOS Project
## Company: GMV Aerospace & Defence S.A.U.
## Licence: GPLv2
##
## Mako template to generate an ASN.1 file for the messages in a ROS package.
##
<% import os %>\
<%                              %>-- Generated from ${os.path.basename(context._with_template.uri)} for package ${pkg.pkg_name}

<%                              %>${pkg.asn_package_name(pkg.pkg_name)} DEFINITIONS ::=
<%                              %>BEGIN

<%                              %>IMPORTS
% for typ in pkg.ImportsBasic:
<%                              %>${typ}${(' FROM TASTE-BasicTypes\n' if loop.last else ', ')}\
% endfor
% for typ in pkg.ImportsExtended:
<%                              %>${typ}${(' FROM TASTE-ExtendedTypes\n' if loop.last else ', ')}\
% endfor
% for req in pkg.required_packages():
%   for typ in pkg.required_types(req):
<%                              %>${pkg.asn_type_name(req, pkg.get_scalar(typ))}${(' FROM '+pkg.asn_package_name(req)+'\n' if loop.last else ', ')}\
%   endfor
% endfor
% for msg in pkg.variable_size_messages():
<%                              %>${pkg.asn_size_constant(msg)}${(', Dummy-'+pkg.asn_package_name(pkg.pkg_name)+'-T FROM UserDefs-'+pkg.asn_package_name(pkg.pkg_name) if loop.last else ', ')}\
% endfor
<%                              %>;
% for msg in pkg.messages():
<%                              %>    -- ================================================================================
<%                              %>    -- Message ${pkg.asn_package_name(pkg.pkg_name)}/${msg}
<%                              %>    -- ================================================================================
<%                              %>${pkg.asn_comment(pkg.full_text(msg))}\
<%                              %>    -- ================================================================================
<%                              %>    -- ASN.1 type for ${pkg.asn_package_name(pkg.pkg_name)}/${msg}
<%                              %>    ${pkg.asn_type_name(pkg.pkg_name, msg)} ::= \
%   if pkg.num_slots(msg) == 1:
%     if pkg.is_scalar(msg,0):
<%                              %>${pkg.to_asn_type(pkg.slot_type(msg,0))}
%     elif pkg.is_fixed_size(msg,0):
%       if pkg.is_octet_type(msg,0):
<%                              %>OCTET STRING (SIZE(${pkg.slot_size(msg,0)}))\
%       else:
<%                              %>SEQUENCE (SIZE(${pkg.slot_size(msg,0)})) OF ${pkg.to_asn_type(pkg.slot_type(msg,0))}\
%       endif
%     elif pkg.is_variable_size(msg,0):
%       if pkg.is_octet_type(msg,0):
<%                              %>OCTET STRING (SIZE(0..${pkg.asn_size_constant(msg)}))\
%       else:
<%                              %>SEQUENCE (SIZE(0..${pkg.asn_size_constant(msg)})) OF ${pkg.to_asn_type(pkg.slot_type(msg,0))}\
%       endif
%     endif

%   else:
<%                              %>SEQUENCE
<%                              %>    {
%     for i in range(pkg.num_slots(msg)):
<%                              %>        ${pkg.asn_field_name(pkg.slot(msg,i))} \
%       if pkg.is_scalar(msg,i):
<%                                                      %>${pkg.to_asn_type(pkg.slot_type(msg,i))}\
%       elif pkg.is_fixed_size(msg,i):
%         if pkg.is_octet_type(msg,i):
<%                                                      %>OCTET STRING (SIZE(${pkg.slot_size(msg,i)}))\
%         else:
<%                                                      %>SEQUENCE (SIZE(${pkg.slot_size(msg,i)})) OF ${pkg.to_asn_type(pkg.slot_type(msg,i))}\
%         endif
%       elif pkg.is_variable_size(msg,i):
%         if pkg.is_octet_type(msg,i):
<%                                                      %>OCTET STRING (SIZE(0..${pkg.asn_size_constant(msg)}))\
%         else:
<%                                                      %>SEQUENCE (SIZE(0..${pkg.asn_size_constant(msg)})) OF ${pkg.to_asn_type(pkg.slot_type(msg,i))}\
%         endif
%       endif
<%                                                      %>${('' if loop.last else ',')}
%     endfor
<%                              %>    }
%   endif
<%                              %>    -- ================================================================================

% endfor
<%                              %>END
