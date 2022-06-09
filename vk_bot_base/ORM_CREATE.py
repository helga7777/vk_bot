import psycopg2
from requests import session
import sqlalchemy as sq
from sqlalchemy import Integer, desc, asc, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://davyd:......@localhost:5432/candidates')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'Users'
    id = sq.Column(sq.Integer, primary_key=True)
    Vk_id = sq.Column(sq.Integer, nullable=False)
    citi = sq.Column(sq.String, nullable=False)
    gender = sq.Column(sq.Integer, nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    Searching_results = relationship('Searching_result', backref='Users')

    def add_user(self, user_Vk_id, user_citi, user_gender, user_age, session=None):
        '''
        Добавляет Vk_id, город, пол, возраст для экземпляра User в базу,
        если данный экземпляр отсутсвует  в базе
        '''
        if session is None:
            session = Session()
        user = session.query(User).filter(User.Vk_id == user_Vk_id).first()
        if user is None:
            user = User(
                        Vk_id=user_Vk_id,
                        citi=user_citi,
                        gender=user_gender,
                        age=user_age
                )
            session.add(user)
        session.commit()
    
    def get_user(self, user_Vk_id, session=None):
        '''
        Ищет экземпляр User в базе по Vk_id и если нет возвращает None,
        если есть возвращает город, пол, возраст
        '''
        if session is None:
            session = Session()
        user = session.query(User.citi, User.gender, User.age).filter(User.Vk_id == user_Vk_id).first()
        if user is None:
            return user
        session.commit()
        return user
        

class Searching_result(Base):
    __tablename__ = 'Searching_results'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    last_name = sq.Column(sq.String, nullable=False)
    link_profile = sq.Column(sq.String, nullable=False)
    is_favorites = sq.Column(sq.Boolean)
    User_id = sq.Column(sq.Integer, sq.ForeignKey('Users.id'))
    Photos = relationship('Photo', backref='Searching_results')

    def add_Searching_results(self, name, last_name, link_profile, user_id, session=None):
        '''
        Добавляет результаты поска name, last_name, link_profile в базу
        '''
        if session is None:
            session = Session()
        search = session.query(Searching_result).filter(
            Searching_result.name == name and Searching_result.last_name == last_name
            ).first()
        if search is None:
            search_id = session.query(User.id).filter(User.Vk_id == user_id).first()
            search = session.query(User).get(search_id)
            search.Searching_results.append(Searching_result(
                                                            name=name,
                                                            last_name=last_name,
                                                            link_profile=link_profile,
                                                            is_favorites = False
                ))
            session.add(search)
        session.commit()

    def add_fivorites(self, name, last_name, bool=True, session=None):
        '''
        Добавляет результаты поиска в избранное
        '''
        if session is None:
            session = Session()
        favorites = session.query(Searching_result).filter(
            Searching_result.name == name and Searching_result.last_name == last_name
            ).all()
        for f in favorites:
            f.is_favorites = bool
        session.commit()

    def get_fivorites(self, user_id, session=None):
        '''
        Возращает список name, last_name избранных пользователей
        '''
        if session is None:
            session = Session()
        search_id = session.query(User.id).filter(User.Vk_id == user_id).first()
        favorites_list = session.query(Searching_result.name, Searching_result.last_name).join(User).filter(
            Searching_result.is_favorites == True and User.id == search_id[0]
            ).all()
        session.commit()
        return favorites_list


class Photo(Base):
    __tablename__ = 'Photos'
    id = sq.Column(sq.Integer, primary_key=True)
    Url_list = sq.Column(sq.String, nullable=False)
    Searching_result_id = sq.Column(sq.Integer, sq.ForeignKey('Searching_results.id'))

    def add_photo(self, name, last_name, url_list, session=None):
        '''
        Добавляет список ссылок на фото в таблицу Photo
        '''
        if session is None:
            session = Session()
        search_id = session.query(Searching_result.id).filter(
            Searching_result.name == name and Searching_result.last_name == last_name
            ).first()
        photo = session.query(Searching_result).get(search_id)
        for p in url_list:
            photo.Photos.append(Photo(Url_list=str(p)))
        session.commit()


if __name__ == '__main__':
    '''
    Инициализация базы
    '''
    session = Session()
    Base.metadata.create_all(engine)
    session.commit()