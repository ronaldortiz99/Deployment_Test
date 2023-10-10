import datetime
from fastapi import HTTPException
import threading
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models,schemas

lock = threading.Lock()
def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, id: int, team: schemas.TeamCreate):
    db_team = db.query(models.Team).filter(models.Team.id == id).first()
    if db_team:
        db_team.name = team.name
        db_team.country = team.country
        db_team.description = team.description
    else:
        db_team = models.Team(name=team.name, country=team.country, description=team.description)
        db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, id: int):
    db_team = db.query(models.Team).filter(models.Team.id == id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
    return "El equipo ha sido eliminado de la base de datos."

def get_competition(db: Session, competition: schemas.CompetitionCreate):
    return db.query(models.Competition).filter(models.Competition.name == competition.name,
                                               models.Competition.sport == competition.sport.name,
                                               models.Competition.category == competition.category.name).first()


def get_competition_by_id(db: Session, id: int):
    return db.query(models.Competition).filter(models.Competition.id == id).first()

def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competition).offset(skip).limit(limit).all()

def create_competition(db: Session, competition: schemas.CompetitionCreate):
    db_competition = models.Competition(name=competition.name,
                                        category=competition.category.name,
                                        sport=competition.sport.name)
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

def update_competition(db: Session, id: int, competition: schemas.CompetitionCreate):
    db_competition = db.query(models.Competition).filter(models.Competition.id == id).first()
    if db_competition:
        db_competition.name = competition.name
        db_competition.sport = competition.sport.name
        db_competition.category = competition.category.name
    else:
        db_competition = models.Competition(name=competition.name,
                                            category=competition.category.name,
                                            sport=competition.sport.name)
        db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

def delete_competition(db: Session, id: int):
    db_competition = db.query(models.Competition).filter(models.Competition.id == id).first()
    if db_competition:
        db.delete(db_competition)
        db.commit()
        return "La competición ha sido eliminado de la base de datos."

def add_team_to_competition(db: Session, team_id: int, competition_id: int):
    team = get_team(db=db,team_id=team_id)
    competition = get_competition_by_id(db=db,id=competition_id)
    if team and competition:
        competition.teams.append(team)
        db.commit()
        return competition

def get_competitions_by_team(db: Session, team_name: str):
    team = get_team_by_name(db=db,name=team_name)
    return db.query(models.Competition).filter(models.Competition.teams.contains(team)).all()

def get_teams_from_competition(db: Session, id: int):
    competition = get_competition_by_id(db=db, id=id)
    if competition:
        return competition.teams

def get_match(db: Session, match: schemas.MatchCreate):
    return db.query(models.Match).filter(models.Match.local_id == match.local.id,
                                         models.Match.visitor_id == match.visitor.id,
                                         models.Match.competition_id == match.competition.id,
                                         models.Match.date == match.date).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()

def get_match_by_id(db: Session, id: int):
    return db.query(models.Match).filter(models.Match.id == id).first()

def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(date=match.date, total_available_tickets=match.total_available_tickets, price=match.price, local_id=match.local.id, visitor_id=match.visitor.id, competition_id=match.competition.id)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match(db: Session, id: int, match: schemas.MatchCreate):
    db_match = db.query(models.Match).filter(models.Match.id == id).first()
    if db_match:
        db_match.date = match.date
        db_match.price = match.price
        db_match.local_id = match.local.id
        db_match.visitor_id =match.visitor.id
        db_match.competition_id = match.competition.id
        db_match.total_available_tickets = match.total_available_tickets
    else:
        db_match = models.Match(date = match.date, total_available_tickets=match.tickets, price=match.price, local_id = match.local.id, visitor_id = match.visitor.id, competition_id = match.competition.id)
        db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, id: int):
    db_match = db.query(models.Match).filter(models.Match.id == id).first()
    if db_match:
        db.delete(db_match)
        db.commit()
        return "El partido ha sido eliminado de la base de datos."

def get_matches_by_team(db: Session, team_name: str):
    db_team = get_team_by_name(db=db, name=team_name)
    db_match = []
    if db_team:
        db_match = db.query(models.Match).filter(or_(models.Match.visitor_id == db_team.id,models.Match.local_id == db_team.id)).all()
    return db_match

def get_matches_by_competition(db: Session, name: str):
    return db.query(models.Match).filter(models.Match.competition.has(name=name)).all()

def get_match_teams_by_id(db: Session, id: int):
    db_match = db.query(models.Match).filter(models.Match.id == id).first()
    if db_match:
        visitor = db.query(models.Team).filter(models.Team.id == db_match.visitor_id).first()
        local = db.query(models.Team).filter(models.Team.id == db_match.local_id).first()
        return {"local": local, "visitor": visitor}

def get_competition_by_match_id(db: Session, id: int):
    db_match = db.query(models.Match).filter(models.Match.id == id).first()
    if db_match:
        return db.query(models.Competition).filter(models.Competition.id == db_match.competition_id).first()

def create_account(db: Session, user: schemas.AccountCreate):
    db_account = models.Account(username=user['username'],password=user['password']
                                ,available_money=user['available_money'],is_admin=user['is_admin'])
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def is_valid_username(db: Session, name: str):
    db_account = db.query(models.Account).filter(models.Account.username == name).first()
    if db_account:
        return False
    return True


def get_orders_user(db: Session, username: str):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if not db_account:
        return "No existe ninguna cuenta con ese nombre de usuario."
    return db_account.orders

def create_order(db: Session, username: str, order: schemas.OrderCreate):
    lock.acquire()
    try:
        db_account = db.query(models.Account).filter(models.Account.username == username).first()
        db_match = db.query(models.Match).filter(models.Match.id == order.match_id).first()

        if db_account and db_match:
            if db_account.available_money - db_match.price * order.tickets_bought >= 0:
                if db_match.total_available_tickets - order.tickets_bought >= 0:
                    db.refresh(db_account)
                    db_account.available_money -= db_match.price * order.tickets_bought
                    db_match.total_available_tickets -= order.tickets_bought

                    db_order = models.Order(tickets_bought=order.tickets_bought, match_id=order.match_id)
                    db_order.username = username
                    db_account.orders.append(db_order)

                    db.add(db_order)
                    db.commit()
                    db.refresh(db_match)
                    db.refresh(db_order)
                    db.refresh(db_account)

                    return db_order
    except Exception as e:
        db.rollback()
        raise e
    finally:
        lock.release()
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_account(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()

def delete_order(db: Session, order: schemas.Order):
    db_order = db.query(models.Order).filter(models.Order.id == order.id).first()
    if db_order:
        db_match = db.query(models.Match).filter(models.Match.id == order.match_id).first()
        if db_match:
            db_match.total_available_tickets += order.tickets_bought
            db.delete(db_order)
            db.commit()
            db.refresh(db_match)
            return "La orden ha sido eliminada de la base de datos."

def delete_account(db: Session, username: str):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if db_account:
        db_orders = db.query(models.Order).filter(models.Order.username == username).all()
        for order in db_orders:
            delete_order(db=db, order=order)
        db.delete(db_account)
        db.commit()
        return "La cuenta ha sido eliminada de la base de datos."
def update_account(db: Session, username: str, user):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if db_account:
        db_account.username = user['username']
        db_account.password = user['password']
        db_account.available_money = user['available_money']
        db_account.is_admin = user['is_admin']
    db.commit()
    db.refresh(db_account)
    return db_account

def get_accounts(db: Session):
    return db.query(models.Account).all()