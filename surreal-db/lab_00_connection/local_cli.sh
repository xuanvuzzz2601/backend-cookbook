#!/bin/bash

# Hiển thị thông báo cho người dùng
echo "🔌 Đang kết nối tới SurrealDB CLI..."
echo "💡 Gõ 'HELP;' để xem các lệnh trợ giúp hoặc 'QUIT;' để thoát."
echo "--------------------------------------------------------"

# Câu lệnh chính thức để gọi SurrealDB CLI kết nối vào Docker Container
# Sử dụng Namespace (ns) là 'cookbook' và Database (db) là 'testing'
docker run --rm \
  --name surrealdb-test \
  -p 8080:8000 \
  -e SURREAL_USER=root \
  -e SURREAL_PASS=root \
  surrealdb/surrealdb:latest \
  start