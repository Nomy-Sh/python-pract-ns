# from sqlmodel import Field, SQLModel
# from sqlmodel import Field, Session, SQLModel, create_engine, select


# # class Hero(SQLModel, table=True):
# #     id: int | None = Field(default=None, primary_key=True)
# #     name: str
# #     secret_name: str
# #     age: int | None = None


# # hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
# # hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
# # hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


# # engine = create_engine("sqlite:///database.db")


# # SQLModel.metadata.create_all(engine)

# # with Session(engine) as session:
# #     session.add(hero_1)
# #     session.add(hero_2)
# #     session.add(hero_3)
# #     session.commit()


# with Session(engine) as session:
#     statement = select(Hero)
#     hero = session.exec(statement).all()
#     print(len(hero))







from sqlmodel import SQLModel, Session, Field, create_engine, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_name: str | None
    address: str | None

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    secret_identity: str | None = Field(index=True)
    team_id: int | None



engine = create_engine('sqlite:///database.db', echo=True)

def create_db_and_model():
    SQLModel.metadata.create_all(engine)


def add_dummy_hero_data(engine):
    hero1 = Hero(name='Spider-man', secret_identity='Peter Parker', team_id=1)
    hero2 = Hero(name='Iron Man', secret_identity='Tony Stark', team_id=1)
    hero3 = Hero(name='Winter Soldier', secret_identity='Buckanan (Bucky) James Barnes', team_id=3)
    
    with Session(engine) as session:
        session.add(hero1)
        session.add(hero2)
        session.add(hero3)
        session.commit()


def add_dummy_team_data(engine):
    team1 = Team(team_name='Avengers', address='Avengers tower, NY, MCU')
    team2 = Team(team_name='Justice Leage', address='Metropolis, DCU')
    team3 = Team(team_name='Avengerz', address='UNK, NY, MCU')

    with Session(engine) as session:
        session.add(team1)
        session.add(team2)
        session.add(team3)
        session.commit()



def read_data(obj):
    with Session(engine) as session:
        # query = select(obj)#.where(id=1)
        # resp = session.exec(query)
        # # print(resp)
        # print('\n'*2, *resp)
        # print(*resp)

        query2 = select(obj)
        resp = session.exec(query2).all()
        # print(resp)
        for r in resp:
            print(r)
        # print('\n', *resp)


        #print(teams)
    #Hero.select().where(Hero.id = 1)

# create_db_and_model()
# add_dummy_team_data(engine)
# add_dummy_hero_data(engine)
# read_data(obj = Team)
read_data(obj = Hero)


def read_data_by_name():
    with Session(engine) as session:
        query2 = select(Hero).where(Hero.secret_identity=='Peter Parker')
        resp = session.exec(query2)
        print('\n', *resp)

# read_data_by_name()