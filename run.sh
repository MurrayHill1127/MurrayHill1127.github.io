#!/bin/bash


script_dir=$(dirname "$0")
cd "$script_dir"


echo "Running Blog::md2html.py..."
python3 blog/md2html.py
if [ $? -ne 0 ]; then
    echo "Blog::md2html failed to run."
    exit 1
fi
echo ""
echo "Running Blog::index.py..."
python3 blog/index.py
if [ $? -ne 0 ]; then
    echo "Blog::index.py.py failed to run."
    exit 1
fi



echo ""
echo "Running WriteUp::md2html.py..."
python3 writeup/md2html.py
if [ $? -ne 0 ]; then
    echo "WriteUp::md2html failed to run."
    exit 1
fi
echo ""
echo "Running WriteUp::index.py..."
python3 writeup/index.py
if [ $? -ne 0 ]; then
    echo "WriteUp::index.py.py failed to run."
    exit 1
fi

echo ""
echo "All scripts executed successfully."
