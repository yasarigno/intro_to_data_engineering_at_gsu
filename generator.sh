#!/bin/bash

# List of positional arguments
list_of_countries=("France" "Germany" "United States" "North Korea" "Syria" "Turkey" "Mexico" "Italy" "Russia")

# Try this as well
list_of_animals=(
    "African elephant" "African lion" "American black bear" "Bald eagle" "Bengal tiger"
    "Blue whale" "Bottlenose dolphin" "Brown bear" "Cheetah" "Chimpanzee" "Common octopus"
    "Dalmatian dog" "Cat" "Chicken" "Cow" "Dog" "Goat" "Pig" "Rabbit" "Sheep" "Emperor penguin"
    "Giant panda" "Giraffe" "Golden retriever" "Gray wolf" "Great white shark" "Grizzly bear"
    "Hippopotamus" "Honey bee" "Horse" "House sparrow" "Human" "Humpback whale" "King cobra"
    "Koala" "Labrador Retriever" "Llama" "Magellanic penguin" "Monarch butterfly""Mountain lion"
    "Orca" "Pug" "Raccoon" "Red fox" "Red kangaroo" "Siberian tiger" "Snow leopard" "Southern elephant seal"
    "Squirrel monkey" "Sumatran orangutan"
)

# Loop through each argument
for art in "${list_of_animals[@]}"
do
    # Run the Python command for each argument
    echo "$art"
    python app.py "$art"
done

# You may need:
# chmod +x generator.sh