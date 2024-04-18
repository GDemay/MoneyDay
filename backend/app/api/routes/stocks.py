from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Stock, StockCreate, StockPublic, StocksPublic, StockUpdate, Message
import typing as t
router = APIRouter()

@router.get("/", response_model=StocksPublic)
def read_stocks(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> t.Any:
    """
    Retrieve stocks.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Stock)
        count = session.exec(count_statement).one()
        statement = select(Stock).offset(skip).limit(limit)
        stocks = session.exec(statement).all()
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return StocksPublic(data=stocks, count=count)

@router.get("/{id}", response_model=StockPublic)
def read_stock(session: SessionDep, current_user: CurrentUser, id: int) -> t.Any:
    """
    Get stock by ID.
    """
    stock = session.get(Stock, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.post("/", response_model=StockPublic)
def create_stock(
    *, session: SessionDep, item_in: StockCreate
) -> t.Any:
    """
    Create new stock.
    """
    stock = Stock(**item_in.dict())
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock

@router.put("/{id}", response_model=StockPublic)
def update_stock(
    *, session: SessionDep, id: int, stock_in: StockUpdate
) -> t.Any:
    """
    Update a stock.
    """
    stock = session.get(Stock, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    update_data = stock_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stock, key, value)
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock

@router.delete("/{id}")
def delete_stock(session: SessionDep, id: int) -> Message:
    """
    Delete a stock.
    """
    stock = session.get(Stock, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    session.delete(stock)
    session.commit()
    return Message(message="Stock deleted successfully")
