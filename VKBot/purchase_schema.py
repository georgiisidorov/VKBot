from sqlalchemy import Column, Integer, BigInteger, String, Float, sql, ForeignKey

from MAIN.utils.db_api.db_gino import TimedBaseModel


class Purchase(TimedBaseModel):
    __tablename__ = 'purchase'
    id = Column(String(100), primary_key=True)
    user_id = Column(BigInteger)
    amount = Column(Float(20))
    currency = Column(String(3))


    query: sql.Select