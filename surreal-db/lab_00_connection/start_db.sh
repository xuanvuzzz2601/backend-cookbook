
# trường hợp này test thì không cần signin nha nếu sign-in thì báo lỗi authen
# docker run --rm --pull always \
#   --name surrealdb-test \
#   -p 8080:8000 \
#   surrealdb/surrealdb:latest start --unauthenticated

# trường hợp set-up authen thì nhớ sign-in account root account này sẽ có toàn quyền 

docker run --rm --pull always \
  --name surrealdb-test \
  -p 8080:8000 \
  -e SURREAL_USER=vuhx \
  -e SURREAL_PASS=123456 \
  surrealdb/surrealdb:latest start