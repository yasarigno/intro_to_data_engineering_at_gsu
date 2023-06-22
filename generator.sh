#!/bin/bash

# List of positional arguments
list_of_articles=("turkey" "france" "mexico" "italy" "russia")

# Loop through each argument
for art in "${list_of_articles[@]}"
do
    # Run the Python command for each argument
    echo "$art"
    python app.py "$art"
done

# use this script as: 
# bash generator.sh

# you may need to run (only for the first time)
# chmod +x generator.sh
