from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session


from . import repository,schemas,models
from .database import SessionLocal, engine
from .utils import get_hashed_password

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.security import OAuth2PasswordRequestForm
from .dependencies import get_current_user,get_current_admin
from fastapi.responses import RedirectResponse
from .utils import verify_password, create_access_token, create_refresh_token

models.Base.metadata.create_all(bind=engine) # Creem la base de dades amb els models que hem definit a SQLAlchemy

app = FastAPI()
app.mount("/static", StaticFiles(directory="services/frontend/dist"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="services/frontend/dist")
@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_teams(db, skip=skip, limit=limit)

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    db_team = repository.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already Exists, Use put for updating")
    else:
        return repository.create_team(db=db, team=team)

@app.get("/team/{team_name}", response_model=schemas.Team)
def read_team(team_name: str,db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.get("/team/{id}", response_model=schemas.Team)
def read_team(id: int,db: Session = Depends(get_db)):
    team = repository.get_team(db=db, team_id=id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.put("/teams/{id}", response_model=schemas.Team)
def update_team(id: int, team: schemas.TeamCreate,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    return repository.update_team(db=db, id=id, team=team)

@app.delete("/teams/{id}")
def delete_team(id: int,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    team = repository.get_team(db=db, team_id=id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.delete_team(db=db, id=id)

@app.get("/competitions/", response_model=list[schemas.Competition])
def read_competition(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_competitions(db, skip=skip, limit=limit)

@app.post("/competitions/", response_model=schemas.Competition)
def create_competition(competition: schemas.CompetitionCreate, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    db_competition = repository.get_competition(db, competition=competition)
    if db_competition:
        raise HTTPException(status_code=400, detail="Competition already Exists, Use put for updating")
    else:
        return repository.create_competition(db=db, competition=competition)

@app.get("/competition/{id}", response_model=schemas.Competition)
def read_competition(id: int,db: Session = Depends(get_db)):
    competition = repository.get_competition_by_id(db=db, id=id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

@app.put("/competitions/{id}", response_model=schemas.Competition)
def update_competition(id: int, competition: schemas.CompetitionCreate,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    return repository.update_competition(db=db, id=id, competition=competition)

@app.delete("/competitions/{id}")
def delete_competition(id: int,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    competition = repository.get_competition_by_id(db=db, id=id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return repository.delete_competition(db=db, id=id)

@app.post("/competitions/{competition_id}/teams/{team_id}", response_model=schemas.Competition)
def add_team_to_competition(competition_id: int, team_id: int, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    competition = repository.get_competition_by_id(db, id=competition_id)
    team = repository.get_team(db, team_id=team_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.add_team_to_competition(db=db,team_id=team_id,competition_id=competition_id)

@app.get("/teams/{team_name}/competitions", response_model=list[schemas.Competition])
def get_competitions(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db=db,name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.get_competitions_by_team(db=db,team_name=team_name)

@app.get("/competitions/{competition_id}/teams", response_model=list[schemas.Team])
def get_teams(competition_id: int, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_id(db=db,id=competition_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return repository.get_teams_from_competition(db=db,id=competition_id)

@app.get("/matches/", response_model=list[schemas.Match])
def read_matches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_matches(db, skip=skip, limit=limit)

@app.get("/match/{id}", response_model=schemas.Match)
def read_matches(id: int,db: Session = Depends(get_db)):
    match = repository.get_match_by_id(db=db, id=id)
    if not match:
        raise HTTPException(status_code=404, detail="Competition not found")
    return match

@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    db_match = repository.get_match(db=db, match=match)
    if db_match:
        raise HTTPException(status_code=400, detail="Match already Exists, Use put for updating")
    else:
        return repository.create_match(db=db, match=match)

@app.put("/matches/{id}", response_model=schemas.Match)
def update_competition(id: int, match: schemas.MatchCreate,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    return repository.update_match(db=db, id=id, match=match)

@app.delete("/matches/{id}")
def delete_match(id: int,db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    match = repository.get_match_by_id(db=db, id=id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return repository.delete_match(db=db, id=id)

@app.get("/teams/{team_name}/matches")
def get_matches_by_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db=db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return repository.get_matches_by_team(db=db, team_name=team_name)

@app.get("/competitions/{competition_name}/matches")
def get_matches_by_competition(competition_name: str, db: Session = Depends(get_db)):
    try:
        return repository.get_matches_by_competition(db=db, name=competition_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Competition not found")

@app.get("/matches/{match_id}/teams")
def get_teams_by_match_id(match_id: int, db: Session = Depends(get_db)):
    return repository.get_match_teams_by_id(db=db,id=match_id)

@app.get("/matches/{match_id}/competition")
def get_competition_by_match_id(match_id: int, db: Session = Depends(get_db)):
    return repository.get_competition_by_match_id(db=db,id=match_id)

@app.post('/account', summary="Create new user", response_model=schemas.Account)
def create_account(data: schemas.AccountCreate, db: Session = Depends(get_db)):
    if not repository.is_valid_username(db=db, name=data.username):
        raise HTTPException(status_code=400, detail="Username not available")
    else:
        user = {
            'username': data.username,
            'password': get_hashed_password(data.password),
            'available_money': data.available_money,
            'is_admin': data.is_admin
        }
        return repository.create_account(db=db, user=user)

@app.get('/orders/{username}', response_model=list[schemas.Order])
def get_orders_user(username: str, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_user)):
    if user.username != username and user.is_admin == 0:
        raise HTTPException(status_code=403, detail="Forbidden Acces")
    return repository.get_orders_user(db=db,username=username)

@app.post('/orders/{username}', response_model=schemas.Order)
def create_order(username: str, order: schemas.OrderCreate, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_user)):
    if user.username != username and user.is_admin == 0:
        raise HTTPException(status_code=403, detail="Forbidden Acces")
    return repository.create_order(db=db,username=username,order=order)

@app.get('/orders', response_model=list[schemas.Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_user)):
    return repository.get_orders(db=db, skip=skip, limit=limit)

@app.get('/account', summary='Get details of currently logged in user', response_model=schemas.SystemAccount)
async def get_me(user: schemas.SystemAccount = Depends(get_current_user)):
    return user

@app.get('/account/{username}', response_model=schemas.Account)
def get_account(username: str, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_user)):
    db_account = repository.get_account(db=db, username=username)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    if user.username != username and user.is_admin == 0:
        raise HTTPException(status_code=403, detail="Forbidden Acces")
    return db_account

@app.delete('/account/{username}')
def delete_account(username: str, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    db_account = repository.delete_account(db=db, username=username)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.put('/account/{username}', response_model=schemas.Account)
def update_account(username: str, account: schemas.AccountCreate, db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_user)):
    if username != account.username:
        if not repository.is_valid_username(db=db, name=account.username):
            raise HTTPException(status_code=400, detail="Username not available")
    user = {
        'username': account.username,
        'password': get_hashed_password(account.password),
        'available_money': account.available_money,
        'is_admin': account.is_admin
    }
    db_account = repository.update_account(db=db, username=username, user=user)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    if user.username != username and user.is_admin == 0:
        raise HTTPException(status_code=403, detail="Forbidden Acces")
    return db_account

@app.get('/accounts', response_model=list[schemas.Account])
def get_accounts(db: Session = Depends(get_db),user: schemas.SystemAccount = Depends(get_current_admin)):
    return repository.get_accounts(db=db)

@app.post('/login', summary="Create access and refresh tokens for user", response_model=schemas.TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    db_account = repository.get_account(db=db, username=username)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not verify_password(password, db_account.password):
         raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(username)
    refresh_token = create_refresh_token(username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

