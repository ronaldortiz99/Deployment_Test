import enum
from .models import sports_list, categories_list
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TeamBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class CompetitionBase(BaseModel):
    name: str
    category: enum.Enum('category', dict(zip(categories_list, categories_list)))
    sport: enum.Enum('sport', dict(zip(sports_list, sports_list)))


class CompetitionCreate(CompetitionBase):
    pass

class Competition(CompetitionBase):
    id: int
    teams: list[Team] = []

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    date: datetime
    price: float
    total_available_tickets: int
    local: Team
    visitor: Team
    competition: Competition


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    username: str
    password: str
    available_money: float
    is_admin: int
class AccountCreate(BaseModel):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=8, max_length=24 ,description="user password")
    available_money: float
    is_admin: int

class Account(AccountBase):

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    match_id: int
    tickets_bought: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class SystemAccount(Account):
    password: str