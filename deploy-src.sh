#!/bin/bash

# Script to sync changes from src folder to remote server
# Server: dataengine@31.193.99.96

# Configuration
REMOTE_USER="dataengine"
REMOTE_HOST="31.193.99.96"
LOCAL_SRC="./src"
REMOTE_DEST="~/src"  # Change this to your desired destination path on the server

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting sync of src folder to ${REMOTE_USER}@${REMOTE_HOST}...${NC}"

# Check if src directory exists
if [ ! -d "$LOCAL_SRC" ]; then
    echo -e "${RED}Error: Directory $LOCAL_SRC does not exist!${NC}"
    exit 1
fi

# Use rsync to sync files
# -a: archive mode (preserves permissions, times, etc.)
# -v: verbose
# -z: compress during transfer
# --delete: delete files in destination that don't exist in source
# --progress: show progress
rsync -avz --progress --delete "$LOCAL_SRC/" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DEST}/"

# Check exit status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Sync completed successfully!${NC}"
else
    echo -e "${RED}✗ Sync failed with exit code $?${NC}"
    exit 1
fi
