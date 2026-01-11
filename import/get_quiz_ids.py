import pymysql

try:
    connection = pymysql.connect(
        host='localhost', user='root', password='',
        database='lophocdhs', port=3307
    )
    with connection.cursor() as cursor:
        # Lay danh sach cac bai Quiz trong khoa hoc ID 3
        sql = """
        SELECT id, itemname 
        FROM mdl_grade_items 
        WHERE courseid = 3 AND itemtype = 'mod' AND itemmodule = 'quiz'
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        print("--- DANH SACH BAI QUIZ TRONG KHOA HOC C++ ---")
        for row in rows:
            print(f"ID: {row[0]} | Ten bai: {row[1]}")
        print("-------------------------------------------")

    connection.close()
except Exception as e:
    print(f"Loi: {e}")