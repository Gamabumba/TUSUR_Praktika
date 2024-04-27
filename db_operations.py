import psycopg2
from psycopg2 import Error


def write_in_db(org_name, org_link, directors_spec, directors_name, phones, emails, address, sites, birth_date, about):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      password="cfnjyby2002",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="partners_db")

        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO partners (org_name, org_link, directors_spec, directors_name, phones, emails, address, sites, birth_date, about) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""" %
                (org_name, org_link, directors_spec, directors_name, phones, emails, address, sites, birth_date, about))

            connection.commit()
            print("Успешно записана строка")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()


def delete_from_db():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      password="cfnjyby2002",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="partners_db")

        with connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM partners"""
            )

            connection.commit()
            print("Успешно удалены строки")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()
