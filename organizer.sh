#!/bin/bash
# organizer.sh - archives .csv files into ./archive and logs actions to organizer.log

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# Create archive dir if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
fi

shopt -s nullglob
csv_files=(*.csv)

for file in "${csv_files[@]}"; do
    # Generate timestamp
    timestamp=$(date +"%Y%m%d-%H%M%S")
    base="${file%.csv}"
    new_name="${base}-${timestamp}.csv"

    # Log action header
    {
      echo "---- ARCHIVE ACTION ----"
      echo "File: $file"
      echo "Timestamp: $timestamp"
      echo "Archived-as: $ARCHIVE_DIR/$new_name"
      echo "Content:"
      cat "$file"
      echo -e "\n"
    } >> "$LOG_FILE"

    # Move and rename
    mv "$file" "$ARCHIVE_DIR/$new_name"
done