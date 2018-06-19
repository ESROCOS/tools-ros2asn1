# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

"""This module provides functions to import ROS types to ESROCOS.

The ROS types are read from the local install and converted to 
equivalent ASN.1 data types for use in TASTE.

"""

from RosAsn1Generator import RosAsn1Generator
import rosmsg
import rospkg
import os
from mako.template import Template


def load_template(filename):
    '''
    Load a mako template, given its file name, from the templates directory.
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    return Template(filename=path)
    

def process_all_messages(out_dir):
    '''Process all available ROS messages and generate ASN.1 types.
    For each package, one .asn file is created with one type per message.
    Additionally, if the message contains variable-sized elements, a
    userdefs-*.asn file is created with parametrized size defaults.
    '''
   
    rospack = rospkg.RosPack()

    asn_template = load_template('package.asn.mako')
    userdefs_template = load_template('userdefs.asn.mako')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Find packages with messages
    packages = sorted([pkg for pkg, _ in rosmsg.iterate_packages(rospack, rosmsg.MODE_MSG)])

    for pkg in packages:
        print('Creating ASN.1 types for {}'.format(pkg))
        
        pkg_obj = RosAsn1Generator(rospack, pkg)

        # ASN.1 types "pkg.asn"
        asn_txt = asn_template.render(pkg=pkg_obj)

        out_file1 = os.path.join(out_dir, pkg+'.asn')
        with open(out_file1, 'w') as fd:
            fd.write(asn_txt)

        # Size constants for variable-sized types "userdefs-pkg.asn"
        userdefs_txt = userdefs_template.render(pkg=pkg_obj)

        out_file2 = os.path.join(out_dir, 'userdefs-'+pkg+'.asn')
        with open(out_file2, 'w') as fd:
            fd.write(userdefs_txt)
        
    return
