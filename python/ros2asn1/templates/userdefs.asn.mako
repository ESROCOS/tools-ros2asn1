## H2020 ESROCOS Project
## Company: GMV Aerospace & Defence S.A.U.
## Licence: GPLv2
##
## Mako template to generate an ASN.1 file for the size connstants for the messages in a ROS package.
##
<% import os %>\
<%                              %>-- Generated from ${os.path.basename(context._with_template.uri)} for package ${pkg.pkg_name}

<%                              %>UserDefs-${pkg.asn_package_name(pkg.pkg_name)} DEFINITIONS ::=
<%                              %>BEGIN

<%                              %>IMPORTS T-UInt32 FROM TASTE-BasicTypes;

<%                              %>    -- Dummy type (TASTE doesn't handle the includes correctly if an ASN.1 file defines only constants)
<%                              %>    Dummy-${pkg.asn_package_name(pkg.pkg_name)}-T ::= T-UInt32

<%                              %>    -- Size constants definitions: to be set according to the application's needs

% for msg in pkg.variable_size_messages():
<%                              %>    -- Size constant for type ${pkg.asn_type_name(pkg.pkg_name, msg)}
<%                              %>    ${pkg.asn_size_constant(msg)} T-UInt32 ::= ${pkg.DefaultMaxSize}

% endfor
<%                              %>END
