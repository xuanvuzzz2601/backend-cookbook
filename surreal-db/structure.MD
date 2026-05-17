📂 backend-cookbook/
└── 📂 01-surrealdb/
    ├── 📄 docker-compose.yml         # Khởi chạy SurrealDB instance
    ├── 📄 README.md                  # Tài liệu hướng dẫn riêng cho phần SurrealDB
    │
    ├── 📂 01-connection/             # PHẦN 1: KẾT NỐI & KHỞI TẠO
    │   ├── 📄 local_cli.sh           # Lệnh kết nối qua Terminal REPL (surreal sql)
    │   ├── 📄 http_api.http          # Gọi API kết nối qua HTTP/REST Client (Postman/Curl)
    │   └── 📄 websocket_python.py    # Kết nối qua Driver SDK (Websocket cho real-time)
    │
    ├── 📂 02-non-relational/         # PHẦN 2: DOCUMENT & SCHEMALESS
    │   ├── 📄 schemaless_crud.surrealql  # CRUD linh hoạt dạng NoSQL JSON
    │   └── 📄 schemafull_strict.surrealql# Định nghĩa bảng nghiêm ngặt (Strict Schema)
    │
    ├── 📂 03-graph-relations/        # PHẦN 3: GRAPH (HỆ THỐNG GỢI Ý)
    │   ├── 📄 setup_nodes_edges.surrealql# Khởi tạo Nodes (User, Item) và Edges (LIKES, VIEWED)
    │   └── 📄 recommendation_queries.surrealql # Câu lệnh truy vấn duyệt đồ thị để gợi ý sản phẩm
    │
    └── 📂 04-vector-search/          # PHẦN 4: VECTOR DB (CHATBOT / RAG)
        ├── 📄 vector_indexing.surrealql  # Định nghĩa MTREE Index cho Vector
        └── 📄 rag_similarity_demo.py # Code Python sinh Embedding và truy vấn Cosine Similarity