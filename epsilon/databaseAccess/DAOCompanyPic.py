from databaseAccess.DAO import DAO


class DAOCompanyPic(DAO):
    # child class of DAO.

    def __init__(self, db):
        super().__init__(db)
    
    def create_pic_table(self) -> None:
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS CompanyPics(
                tid INTEGER not null,
                pic LONGBLOB,
                constraint CompanyPics_pk
                primary key (tid))''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        super().add_foreign_key("CompanyPics", "tid", "Company")
    

    def add_cpic(self, tid:int, file) -> None:
        self.modify_data('''INSERT INTO CompanyPics (tid, pic) 
                            VALUES (%s,%s)''',(tid,file))
    
    def get_cpic(self, tid:int):
        data = self.get_data('''SELECT pic FROM CompanyPics WHERE tid = %s''',(tid,))
        if data:
            return data[0][0]
        return None
    
    def edit_cpic(self, tid:int, file) -> None:
        self.modify_data('''UPDATE CompanyPics SET pic = %s WHERE tid = %s''', (file,tid))
    