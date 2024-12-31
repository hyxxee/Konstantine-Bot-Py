#!/bin/bash

# File query GraphQL
QUERY_FILE="anime_query.graphql"
# File variabel
VARIABLES_FILE="variables.json"

# Membaca query dari file dan mengganti baris baru dengan \n
QUERY=$(sed ':a;N;$!ba;s/\n/\\n/g' "$QUERY_FILE")

# Membaca variabel dari file
VARIABLES=$(cat "$VARIABLES_FILE")

# Mengirim query ke AniList API
RESPONSE=$(curl -s -X POST https://graphql.anilist.co \
-H "Content-Type: application/json" \
-d @<(cat <<EOF
{
    "query": "$QUERY",
    "variables": $VARIABLES
}
EOF
))

# Memproses respons dengan jq
echo "$RESPONSE" | jq '.data.Media'