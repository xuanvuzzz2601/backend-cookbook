## 📁 Chi tiết Phần 1: Modern Databases (Focus: SurrealDB)

**SurrealDB** là một cơ sở dữ liệu Multi-model (Đa mô hình) thế hệ mới, kết hợp sức mạnh của Relational (Quan hệ), Document (Tài liệu), Graph (Đồ thị) và đặc biệt là hỗ trợ **Vector Search** — cực kỳ tối ưu cho các bài toán làm Chatbot và Recommender Systems.

- **Link GitHub chính thức:** [github.com/surrealdb/surrealdb](https://github.com/surrealdb/surrealdb)

### 🌟 Lý do chọn SurrealDB

Đối với một AI Engineer, với sự phát triển tốc độ cực nhanh của AI và các yêu cầu ngày càng cao về tốc độ phản hồi, sự ổn định và nhiều tác vụ phức tạp như các hệ thống thông minh (Chatbot, Recommendation), SurrealDB mang lại những lợi thế vượt trội mà các DB truyền thống không có được:

1. **Tất cả trong một (All-in-One Multi-model):** Bạn không cần phải vận hành và bảo trì đồng thời Postgres (Relational), MongoDB (Document), Neo4j (Graph) và Pinecone (Vector DB) riêng biệt nữa. SurrealDB tích hợp tất cả các mô hình này trong một công cụ duy nhất, giúp kiến trúc hệ thống cực kỳ gọn nhẹ.
2. **Hỗ trợ Vector Search gốc (Native Vector Search):** Đây là "vũ khí tối tân" cho các ứng dụng Generative AI/LLM. Bạn có thể lưu trữ các Vector Embedding (từ OpenAI, BERT, v.v.) và thực hiện tìm kiếm tương đồng (Cosine, Euclidean, Manhattan distance) bằng câu lệnh SurrealQL trực tiếp, giải quyết bài toán RAG cho Chatbot một cách mượt mà.
3. **Mối quan hệ Đồ thị (Graph Relations) không cần JOIN:** Bạn có thể thiết lập liên kết trực tiếp giữa các bảng dữ liệu bằng cấu trúc Node-Edge-Node (Ví dụ: `User` -> `LIKES` -> `Product`). Cú pháp truy vấn Graph của SurrealDB cực kỳ tường minh và tối ưu hiệu năng, rất thích hợp để xây dựng ma trận tương tác cho Recommender Systems.
4. **Thời gian thực (Real-time Live Queries):** Tích hợp sẵn cơ chế lắng nghe thay đổi dữ liệu (Live Queries). Nhờ đó, Backend có thể stream tin nhắn mới của Chatbot về phía người dùng theo thời gian thực mà không cần cấu hình thêm các hệ thống Pub/Sub phức tạp như Redis hay Kafka.
5. **Hiệu năng vượt trội:** Được viết hoàn toàn bằng **Rust**, mang lại tốc độ xử lý nhanh, an toàn về bộ nhớ (memory-safe) và tiêu tốn cực ít tài nguyên phần cứng.

---

### 🚀 Cách cài đặt SurrealDB

SurrealDB hỗ trợ cài đặt đa nền tảng một cách nhanh chóng thông qua các phương thức sau:

#### Cách 1: Sử dụng Docker (Khuyến khích cho môi trường Development)
Cách nhanh nhất để chạy SurrealDB mà không cần cài đặt trực tiếp lên máy:

* **Chạy nhanh phiên bản In-Memory (Dữ liệu mất khi tắt DB, phù hợp để test):**
  ```bash
  docker run --rm --name surrealdb -p 8000:8000 surrealdb/surrealdb:latest start --user root --pass root memory