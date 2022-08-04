import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="J3S6x773",
        host="127.0.0.1",
        port="5432",
        database="sf_test",
    )
    cursor = connection.cursor()

# -----------------------------------------------

#    postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s, %s, %s)"""  
#    record_to_insert = (5, 'One Plus 6', 950)  
#    cursor.execute(postgres_insert_query, record_to_insert)  
#    connection.commit()  
#    count = cursor.rowcount  
#    print (count, "Record inserted successfully into mobile table")

#    postgreSQL_select_Query = "select model from mobile"  
#    cursor.execute(postgreSQL_select_Query)  
#    mobile_records = cursor.fetchall()   
#    connection.commit()
#    print(mobile_records)

# Добавление новых строк  
#    postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""  
#    records_to_insert = [  
#        (1, 'Iphone XS', 1050),  
#        (2, 'Nutella', 30),  
#        (3, 'Pixel', 970)  
#    ]  
#    for record in records_to_insert:  
#        cursor.execute(postgres_insert_query, record)  
#    
#    # Обновление строк  
#    postgreSQL_update_Query = "update mobile set price = 900 where price > 900"  
#    cursor.execute(postgreSQL_update_Query)  
#    connection.commit() 
#    print(cursor.rowcount)
#    query = """delete from mobile where id = %s"""  
#    cursor.execute(query, (2,))  
#    connection.commit() 

# Удалим все данные (без условия)  
#    cursor.execute("DELETE FROM mobile")
#    
    # Теперь вставим строки в таблицу
#    sql_insert_query = """ INSERT INTO mobile (id, model, price) VALUES (%s,%s,%s) """  
#    records_to_insert = [  
#        (1, 'Iphone XS', 1050),  
#        (2, 'Nutella', 30),  
#        (3, 'Pixel', 970)  
#    ]  
#   result = cursor.executemany(sql_insert_query, records_to_insert)  
#    connection.commit()  

#    sql_update_query = """ UPDATE  mobile set model = %s where model = %s """  
#    records_to_update = [  
#        ('Nutella', 'Iphone XS',),  
#        ('Nutella', 'Pixel',)  
#    ]  
#    result = cursor.executemany(sql_update_query, records_to_update)  
#    connection.commit()  

# Найдём список цен, которые не удовлетворяют нашему условию  
#    cursor.execute("select price from mobile where price not between 900 and 1000")  
#    prices_to_delete = cursor.fetchall()  
    
    # Теперь удалим строки с найденными ценами  
#    sql_delete_query = """ DELETE FROM mobile WHERE price = %s """  
#    result = cursor.executemany(sql_delete_query, prices_to_delete)  
#    connection.commit()  

#    with open('module48/mobile.csv', 'r') as f:  
#        cursor.copy_from(f, 'mobile', sep=',')  
#    connection.commit()  

    with open("module48/mobile_2.csv", 'w') as f:  
        cursor.copy_to(f, 'mobile', sep=',')  
    connection.commit()

#------------------------------------------------
        
except (Exception, psycopg2.Error) as error:
    if connection:
        print("Error", error)
finally:
    if connection:
        cursor.close()
        connection.close()