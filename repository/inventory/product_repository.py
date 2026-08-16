# internal's import's
from database.connection import DatabaseConnection
from domain.inventory.product import Product
from domain.inventory.category import Category

class ProductRepository:
    '''Reponsável por coordenar os processos de persistência da classe Product.'''
    def save(self, product: Product) -> None:

        connection = DatabaseConnection.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO product (
                    product_name,
                    category_id,
                    cost_price,
                    sale_value
                )
                VALUES (%s, %s, %s, %s)
                """,    
                (
                    product.name,
                    product.category.id,
                    product.cost_price,
                    product.sale_value
                )
            )
    
            connection.commit()
    
        finally:
            connection.close()
                  
    def reconstruct(self):
        
        connection = DatabaseConnection.get_connection()
        
        try:
            cursor = connection.cursor()
            
            cursor.execute(
                """
                SELECT
                    product.product_id,
                    product.product_name,
                    product.cost_price,
                    product.sale_value,
                    product.available_quantity,
                    product.product_status,
                    category.category_name,
                    category.category_id
                    
                FROM PRODUCT
                JOIN CATEGORY
                ON product.category_id = category.category_id
                ORDER BY product_id;
                """
            )
        
            rows = list(cursor.fetchall())
            products: list[Product] = []
            
            for row in rows:
                product_id = row[0]
                product_name = row[1]
                product_cost_price = row[2]
                product_sale_value = row[3]
                product_available_quantity = row[4]
                product_status = row[5]
                category_name = row[6]
                category_id = row[7]
                
                category = Category.restore(category_name, category_id)
                
                product = Product.restore(product_id, 
                                          product_name, 
                                          category,
                                          product_available_quantity, 
                                          product_sale_value, 
                                          product_cost_price, 
                                          product_status)
                
                products.append(product)
                
            return products
        
        finally:
            connection.close()
            
    def save_a_edit(self, product: Product) -> None:

            connection = DatabaseConnection.get_connection()

            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    UPDATE product
                    SET
                        product_name = %s,
                        category_id = %s,
                        cost_price = %s,
                        sale_value = %s,
                        available_quantity = %s,
                        product_status = %s
                    WHERE product_id = %s  
                    """,
                    (
                        product.name,
                        product.category.id,
                        product.cost_price,
                        product.sale_value,
                        product.available_quantity,
                        product.status,
                        product.id
                    )
                )
        
                connection.commit()
        
            finally:
                connection.close()