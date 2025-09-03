import sqlite3
import asyncio

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("gbi_database.db", check_same_thread=False)
        with self.conn:
            self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Clients (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT NOT NULL, lname TEXT NOT NULL, email TEXT NULL, cell TEXT NOT NULL UNIQUE, address TEXT NULL)")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            order_code TEXT,
                            description TEXT,  
                            date BLOB, 
                            client_id INTEGER, 
                            status BOOLEAN,
                            amount FLOAT, FOREIGN KEY (client_id) REFERENCES Clients (id))""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS OrderItem (
                            item TEXT, 
                            order_id INTEGER,
                            qty INTEGER,
                            colors INTEGER,
                            FOREIGN KEY (order_id) REFERENCES Orders (id)
                            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Pantones (code TEXT UNIQUE, name TEXT UNIQUE,hex TEXT UNIQUE)""")
        
    def createOrder(self, order_code, description, date, client, status=False):
        try:
            self.cursor.execute("""INSERT INTO Orders (order_code, description, date, client_id, status)
                                VALUES (?,?,?,?,?)""", (order_code, description, date, client, status))
            self.conn.commit()
            return True
        except Exception as e:
            return False
        
    def addPantone(self, code:str, name:str, hex:str):
        try:
            self.cursor.execute("""INSERT INTO Pantones (code,name,hex) VALUES (?,?,?)""",
                                (code,name,hex))
            self.conn.commit()
        except Exception as e:
            print(e)

    async def getPantones(self):
        await asyncio.sleep(1)
        self.cursor.execute("SELECT * FROM Pantones")
        return self.cursor.fetchall()

    def createOrderItem(self, item, order_id, qty, colors):

        self.cursor.execute("""INSERT INTO OrderItem (item, order_id, qty, colors)
                            VALUES (?,?,?,?)""", (item, order_id, qty, colors))
        self.conn.commit()

    def getClientById(self, id : int):
        self.cursor.execute(f"SELECT * FROM Clients WHERE id=?", (id,))
        return self.cursor.fetchone()
    
    def getClientByPhone(self, phone):
        self.cursor.execute(f"SELECT * FROM Clients WHERE cell=?", (phone,))
        return self.cursor.fetchone()[0]

    def createClient(self, fname, lname, email, cell, address):
        if email == "":
            email = "no_email@gbinks.com"
        elif address == "":
            address = "No Address"
        try:
            self.cursor.execute("""INSERT INTO Clients (fname, lname, email, cell, address)
                                VALUES (?,?,?,?,?)""", (fname, lname, email, cell, address))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def deleteClient(self, id: int):
        try:
            self.cursor.execute(f"DELETE FROM Clients WHERE id={id}")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

        
    def editClient(self, id : int, fname=None, lname=None, email=None, cell=None, address=None):
        
        current_data = [i for i in self.getClientById(id)[1:]]

        if fname != None:
            current_data[0] = fname
        if lname != None:
            current_data[1] = lname
        if email != None:
            current_data[2] = email
        if cell != None:
            current_data[3] = cell
        if address != None:
            current_data[4] = address
        
        new_data = tuple(current_data)
        try:
            self.cursor.execute(f"UPDATE Clients SET fname=?, lname=?, email=?, cell=?, address=? WHERE id={id}", new_data)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def updateOrderStatus(self, id, status):
        try:
            self.cursor.execute(f"UPDATE Orders SET status=? WHERE id={id}", (status,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getClients(self):
        self.cursor.execute("SELECT * FROM Clients")
        return self.cursor.fetchall()

    def getAllOrders(self):
        self.cursor.execute("SELECT * FROM Orders")
        return self.cursor.fetchall()
    
    def getOrderByCode(self, code):
        self.cursor.execute(f"SELECT * FROM Orders WHERE order_code=?", (code,))
        return self.cursor.fetchone()
    
    def deleteOrder(self, id: int):
        try:
            self.cursor.execute(f"DELETE FROM Orders WHERE id={id}")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def __del__(self):
        self.cursor.close()
        self.conn.close()

# db = Database()
# print(db.getPantones())
# db.editClient(1,address='Chiredzi')
# print(db.getClientById(2))
# print(db.getOrderByCode("djh575"))

# db.createOrder('djh575', "hsjkhfsdhfklsdjklfj", '12/56/2025', 1, False)
# db.createClient("Cathbert", 'Mutaurwa', "cmutaurwa@gbi.com", '0716067144', '1198 Chikangwe, Karoi')
# print(db.getAllOrders())
# print(db.getClients())