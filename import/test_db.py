import pymysql

print("(1) Bat dau kiem tra voi PyMySQL...")

try:
    print("(2) Dang mo ket noi den Port 3307...")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='lophocdhs',
        port=3307,
        connect_timeout=10
    )
    
    print("(3) ===> CHUC MUNG: Ket noi thanh cong!")
    connection.close()

except pymysql.MySQLError as e:
    print(f"(X) LOI DATABASE: {e}")
except Exception as e:
    print(f"(X) LOI KHAC: {e}")

print("(4) Ket thuc kiem tra.")