from databaseAccess.DAO import DAO


class DAOProfilePic(DAO):
    # child class of DAO.

    def __init__(self, db):
        super().__init__(db)
    
    def create_pic_table(self) -> None:
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS ProfilePics(
                uid INTEGER not null,
                pic LONGBLOB,
                constraint ProfilePics_pk
                primary key (uid))''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        super().add_foreign_key("ProfilePics", "uid", "Users")
    

    def add_pic(self, uid:int, file) -> None:
        self.modify_data('''INSERT INTO ProfilePics (uid, pic) 
                            VALUES (%s,%s)''',(uid,file))
    
    def get_pic(self, uid:int):
        data = self.get_data('''SELECT pic FROM ProfilePics WHERE uid = %s''',(uid,))
        if data:
            return data[0][0]
        return None
    
    def edit_pic(self, uid:int, file) -> None:
        self.modify_data('''UPDATE ProfilePics SET pic = %s WHERE uid = %s''', (file,uid))
    