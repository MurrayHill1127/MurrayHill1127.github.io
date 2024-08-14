#!/bin/bash

cd Entry/ || { echo "Failed to enter Entry/ directory"; exit 1; }

for file in *.md; do
    if [ ! -f "$file" ]; then
        echo "No .md files found in Entry/ directory."
        continue
    fi

    echo "Processing metadata for $file..."
    python3 ../Scripts/meta.py $file
    if [ $? -ne 0 ]; then
        echo "Failed to process metadata for $file"
        continue
    fi

    echo "Converting $file to HTML..."
    python3 ../Scripts/md2html.py 
    if [ $? -ne 0 ]; then
        echo "Failed to convert $file to HTML"
        continue
    fi

    echo "Finished processing $file"
done

cd ../Scripts/ || { echo "Failed to enter Scripts/ directory"; exit 1; }

echo "Generating archive index..."
python3 archive_index.py
if [ $? -ne 0 ]; then
    echo "Failed to generate archive index"
    exit 1
fi

echo "Generating category index..."
python3 category_index.py
if [ $? -ne 0 ]; then
    echo "Failed to generate category index"
    exit 1
fi

echo "All tasks completed successfully!"
