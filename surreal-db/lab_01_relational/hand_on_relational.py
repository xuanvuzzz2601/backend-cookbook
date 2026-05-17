import asyncio
import logging
import json
from datetime import datetime
# Import Connection Manager từ Bài 1 của bạn
from lab_00_connection.connection import AsyncSurrealDB  
from surrealdb.errors import AlreadyExistsError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# async def setup_schema(db_client: AsyncSurrealDB):
#     """Bước 1: Khởi tạo cấu trúc bảng dạng Schema-full và tạo Unique Index"""
#     logger.info("--- Thiết lập Schema & Ràng buộc ---")
    
#     # 1. Định nghĩa bảng user (Schema-full)
#     await db_client.db.query("DEFINE TABLE user SCHEMAFULL;")
#     await db_client.db.query("DEFINE FIELD name ON TABLE user TYPE string;")
#     await db_client.db.query("DEFINE FIELD email ON TABLE user TYPE string;")
#     # Tạo Unique Index cho email
#     await db_client.db.query("DEFINE INDEX user_email_unique ON TABLE user COLUMNS email UNIQUE;")

#     # 2. Định nghĩa bảng post (Quan hệ 1-N với user thông qua Record Link)
#     await db_client.db.query("DEFINE TABLE post SCHEMAFULL;")
#     await db_client.db.query("DEFINE FIELD title ON TABLE post TYPE string;")
#     await db_client.db.query("DEFINE FIELD author ON TABLE post TYPE record<user>;")

#     # 3. Định nghĩa bảng product
#     await db_client.db.query("DEFINE TABLE product SCHEMAFULL;")
#     await db_client.db.query("DEFINE FIELD name ON TABLE product TYPE string;")
#     await db_client.db.query("DEFINE FIELD price ON TABLE product TYPE number;")


async def test_crud_and_unique_constraint(db_client: AsyncSurrealDB):
    """Bước 2: Test chèn dữ liệu và kiểm tra ràng buộc Unique"""
    logger.info("--- Test CRUD & Ràng buộc Unique ---")
    
    # Chèn user thành công
    await db_client.db.query("CREATE user:vu SET name = 'Vũ', email = 'vu@zalopay.vn';")
    await db_client.db.query("CREATE user:nha SET name = 'Nhã', email = 'nha@example.com';")
    
    # TEST CASE: Cố tình chèn trùng email để kiểm tra Unique Constraint
    try:
        await db_client.db.query("CREATE user:trung_lap SET name = 'Vũ Fake', email = 'vu@zalopay.vn';")
    except Exception as e:
        logger.info(f"✅ Thành công: Hệ thống chặn trùng email đúng như kỳ vọng! Lỗi: {e}")


async def test_one_to_many_and_fetch(db_client: AsyncSurrealDB):
    """Bước 3: Test quan hệ 1-N và truy vấn thay thế JOIN bằng FETCH"""
    logger.info("--- Test Quan hệ 1-N & FETCH (Thay thế JOIN) ---")
    
    # Tạo bài viết gắn với ID của user:vu
    await db_client.db.query("CREATE post:p1 SET title = 'Hands-on SurrealDB với Relational', author = user:vu;")
    await db_client.db.query("CREATE post:p2 SET title = 'Kiến trúc AI Agent System', author = user:vu;")
    await db_client.db.query("CREATE post:p3 SET title = 'Bài viết của Nhã', author = user:nha;")

    # Thực hiện truy vấn FETCH (Tương đương INNER JOIN trong SQL)
    response = await db_client.db.query("SELECT *, author.* FROM post FETCH author;")
    posts = response[0]['result']
    
    print("\n[FETCH RESULT] Danh sách bài viết và thông tin tác giả kèm theo:")
    for post in posts:
        # Nhờ FETCH, trường author không còn là một chuỗi 'user:vu' nữa mà là một Dict đầy đủ thông tin
        author_name = post.get('author', {}).get('name', 'Ẩn danh')
        print(f" - Bài viết: '{post['title']}' | Tác giả: {author_name}")
    print("")


async def test_many_to_many_graph(db_client: AsyncSurrealDB):
    """Bước 4: Test quan hệ N-N sử dụng Graph Edge (Thay thế Junction Table)"""
    logger.info("--- Test Quan hệ N-N bằng Graph Edges (RELATE) ---")
    
    # Tạo sản phẩm
    await db_client.db.query("CREATE product:laptop SET name = 'MacBook Pro', price = 2000;")
    await db_client.db.query("CREATE product:phone SET name = 'iPhone 16', price = 1000;")

    # Tạo mối quan hệ Mua Hàng (user mua product) bằng lệnh RELATE
    # Thêm meta-data cho mối quan hệ này (số lượng và thời gian)
    await db_client.db.query("""
        RELATE user:vu->orders->product:laptop 
        SET quantity = 1, created_at = time::now();
    """)
    await db_client.db.query("""
        RELATE user:vu->orders->product:phone 
        SET quantity = 2, created_at = time::now();
    """)
    await db_client.db.query("""
        RELATE user:nha->orders->product:laptop 
        SET quantity = 5, created_at = time::now();
    """)

    # TRUY VẤN XUÔI: Tìm các sản phẩm mà user:vu đã đặt mua
    vu_orders_query = await db_client.db.query("SELECT ->orders->product.* AS purchased_products FROM user:vu;")
    vu_products = vu_orders_query[0]['result'][0]['purchased_products']
    print(f"[GRAPH XUÔI] Sản phẩm user:vu đã đặt mua: {[p['name'] for p in vu_products]}")

    # TRUY VẤN NGƯỢC: Tìm xem những ai đã đặt mua sản phẩm product:laptop
    laptop_buyers_query = await db_client.db.query("SELECT <-orders<-user.* AS buyers FROM product:laptop;")
    laptop_buyers = laptop_buyers_query[0]['result'][0]['buyers']
    print(f"[GRAPH NGƯỢC] Những user đã mua MacBook Pro: {[b['name'] for b in laptop_buyers]}\n")


async def clear_data(db_client: AsyncSurrealDB):
    """Dọn dẹp data sau khi test để có thể chạy lại script nhiều lần"""
    await db_client.db.query("REMOVE TABLE user;")
    await db_client.db.query("REMOVE TABLE post;")
    await db_client.db.query("REMOVE TABLE product;")
    await db_client.db.query("REMOVE TABLE orders;")


async def main():
    url = "ws://localhost:8080"
    username = "root"
    password = "root"
    
    # Sử dụng Context Manager async (`async with`) để tự động đóng connection khi kết thúc
    async with AsyncSurrealDB(url, username, password) as db_client:
        # 0. Dọn dẹp dữ liệu cũ (nếu có)
        await clear_data(db_client)
        
        # 1. Khởi tạo cấu trúc
        await setup_schema(db_client)
        
        # 2. Chạy các kịch bản test quan hệ
        await test_crud_and_unique_constraint(db_client)
        await test_one_to_many_and_fetch(db_client)
        await test_many_to_many_graph(db_client)

async def main():
    url = "ws://localhost:8080"

    user_name = "vuhx"
    password = "123456"

    db_client = AsyncSurrealDB(url, user_name, password)

    await db_client.connect()

    await setup_schema(db_client)


async def setup_schema(db_client):
    queries = """
    DEFINE TABLE IF NOT EXISTS user SCHEMAFULL;

    DEFINE FIELD IF NOT EXISTS username
    ON TABLE user
    TYPE string;

    DEFINE INDEX IF NOT EXISTS idx_username
    ON TABLE user
    COLUMNS username
    UNIQUE;
    """

    await db_client._db.query(queries)
    result = await db_client._db.query(
                                        "INFO FOR TABLE user;"
                                    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())