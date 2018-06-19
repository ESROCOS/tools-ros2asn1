echo "Test for ros2asn1_generate.py"
echo ""

PYTHONPATH=../python:$PYTHONPATH
mkdir -p out_asn out_c

echo "Run ASN.1 generation"
../python/ros2asn1_generate.py out_asn
echo "Done."
echo ""

echo "Run ASN.1 compilation to C"
asn1.exe -c -o out_c -atc out_asn/* taste-types/*
echo "Done."
