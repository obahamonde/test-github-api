#!/bin/bash

# Function to get hard drive usage
get_disk_usage() {
    df -P | awk 'NR > 1 {print "{\"filesystem\": \""$1"\", \"size\": \""$2"\", \"used\": \""$3"\", \"available\": \""$4"\", \"percentage\": \""$5"\"},"}'
}

# Get CPU cores
cpu_cores=$(grep -c ^processor /proc/cpuinfo)

# Get total available memory
total_memory=$(free -h --si | awk '/^Mem:/{print $2}')

# Get disk usage in JSON array format
disk_usage=$(get_disk_usage)

# Assemble the JSON output
json_output=$(cat <<EOF
{
    "cpu_cores": $cpu_cores,
    "total_memory": "$total_memory",
    "disk_usage": [
        ${disk_usage%?}
    ]
}
EOF
)

echo "$json_output"
