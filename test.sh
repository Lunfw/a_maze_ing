#!/bin/bash
# test_all_configs.sh

echo "Testing all configurations..."
echo "================================"

for config in tests/test_configs/*.txt; do
	echo ""
	echo "Testing: $config"
	echo "---"
	python3 a_maze_ing.py "$config"
	echo "================================"
done
