# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

install(PROGRAMS "ros2asn1_generate.py" DESTINATION "bin")
install(DIRECTORY "ros2asn1"
        DESTINATION "lib/python"
        FILES_MATCHING 
        PATTERN "*.py" 
        PATTERN "*.mako"
        PATTERN "__pycache__" EXCLUDE)
