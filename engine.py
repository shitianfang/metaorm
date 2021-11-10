import asyncpg

class PGEngine:
    async def make_session(self,db_config):
        '''
            db_config is dict

            'host': '<host>',
            'user': '<username>',
            'password': '<password>',
            'port': '<port>',
            'database': '<database>'

            return session
        '''
        return await asyncpg.create_pool(**db_config)
    
    async def close_session(self):
        await self.session.close()

    async def __init__(self,app,db_config):
        config = app.config["DB_CONFIG"] if "DB_CONFIG" in app.config else db_config
        if not config:
            raise Exception("not db config")
            
        self.session = await self.make_session(db_config)

    # 第二个参数为limit
    async def select(self,sql,*args):
        async with self.session.acquire() as con:
            return await con.fetch(sql,*args)
    
    async def execute(self,sql,*args):
        async with self.session.acquire() as con:
            return await con.execute(sql,*args)

        

        