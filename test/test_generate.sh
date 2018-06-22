echo "Test for ros2asn1_generate.py"
echo ""

PYTHONPATH=../python:$PYTHONPATH

echo "Clear old results"
rm -rf out_asn out_c
mkdir -p out_asn out_c
echo "Done."
echo ""

echo "Run ASN.1 generation"
../python/ros2asn1_generate.py out_asn
echo "Done."
echo ""

echo "Patch userdefs-visualization_msgs.asn to reduce size"
sed -i "s/60/10/g" out_asn/userdefs-visualization_msgs.asn
echo "Done."
echo ""

echo "Run ASN.1 compilation to C"
asn1.exe -c -o out_c -uPER -atc out_asn/* taste-types/*
echo "Done."
echo ""

echo "Compile C code"
cd out_c
make
cd ..
echo "Done."
echo ""

echo "Run ASN.1 unit tests"
./out_c/mainprogram
echo "Done."
echo ""
