# Bài 2: Thao tác Dữ liệu Quan hệ với SurrealDB (Relational Cookbook)

Tài liệu này hướng dẫn cách ánh xạ tư duy từ hệ quản trị cơ sở dữ liệu quan hệ truyền thống (RDBMS như MySQL, PostgreSQL) sang cú pháp SurQL của SurrealDB, tận dụng tối đa sức mạnh của **Record Links** (thay thế Foreign Key) và **Graph Edges** (thay thế Junction Table).

## 📌 Bài Toán Thiết Kế (Database Schema)
Chúng ta xây dựng một hệ thống Blog/E-commerce thu nhỏ gồm 3 thực thể:
1. `user`: Người dùng (Tác giả).
2. `post`: Bài viết (Mỗi bài viết thuộc về **1** tác giả -> Quan hệ 1-N).
3. `product`: Sản phẩm mà người dùng có thể "Mua/Đặt hàng" (Quan hệ N-N giữa `user` và `product`).

---

## 🔄 Bản Đồ Ánh Xạ Tư Duy (RDBMS vs SurrealDB)

| Khái niệm | RDBMS (MySQL / PostgreSQL) | SurrealDB (SurQL) |
| :--- | :--- | :--- |
| **Định nghĩa bảng** | `CREATE TABLE user (...)` | `DEFINE TABLE user SCHEMAFULL;` |
| **Khóa ngoại (1-N)**| `FOREIGN KEY (author_id) REFERENCES user(id)` | `DEFINE FIELD author ON post TYPE record<user>;` |
| **Bảng trung gian (N-N)** | `CREATE TABLE orders (user_id, product_id, ...)` | Không cần bảng trung gian. Dùng **Graph Edge**: `RELATE user->orders->product` |
| **Phép liên kết dữ liệu**| `SELECT * FROM post JOIN user ON ...` | Dùng toán tử `FETCH`: `SELECT * FROM post FETCH author;` |

---

## 🛠️ Các Kịch Bản Kiểm Thử & Thực Hành (Test Cases)

### 1. Schema-full & Ràng buộc Duy nhất (Unique)
SurrealDB mặc định là Schema-less, nhưng để làm việc như một DB quan hệ, ta ép nó về **Schema-full** để kiểm soát chặt chẽ kiểu dữ liệu và ngăn chặn dữ liệu rác.
*   **Cú pháp:** `DEFINE TABLE user SCHEMAFULL;`
*   **Unique Index:** Tránh trùng lặp các trường định danh như `email`.

### 2. Quan hệ 1-N (Record Link) & Phép JOIN (FETCH)
Thay vì lưu `author_id` dưới dạng một chuỗi hoặc số nguyên rồi thực hiện phép `JOIN` tốn tài nguyên, SurrealDB lưu trực tiếp **ID Pointer** (ví dụ: `user:vu`). 
*   Khi truy vấn, từ khóa `FETCH author` sẽ tự động điền (populate) toàn bộ thông tin của user đó vào kết quả một cách tối ưu.

### 3. Quan hệ N-N (Graph Edge)
Đối với quan hệ nhiều-nhiều (ví dụ: Người dùng đặt mua sản phẩm), thay vì tạo bảng `orders` thủ công, ta dùng lệnh `RELATE`. Mối quan hệ này có thể lưu trữ thuộc tính riêng (ví dụ: số lượng mua `quantity`, thời gian mua `created_at`).
*   **Truy vấn xuôi:** Tìm các sản phẩm mà User A đã mua (`SELECT ->orders->product.* FROM user:A`).
*   **Truy vấn ngược:** Tìm danh sách khách hàng đã mua Sản phẩm B (`SELECT <-orders<-user.* FROM product:B`).