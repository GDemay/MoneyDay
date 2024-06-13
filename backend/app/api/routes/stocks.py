import typing as t
from datetime import date

import yfinance as yf
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    Stock,
    StockCreate,
    StockPublic,
    StocksPublic,
    StockUpdate,
    WealthData,
    WealthDataResponse,
)

router = APIRouter()


@router.get("/wealth", response_model=WealthDataResponse)
def compute_wealth(session: SessionDep) -> WealthDataResponse:
    """
    Compute the total wealth based on the user's stock holdings.
    """
    # Get all the stocks
    stocks = session.exec(select(Stock)).all()

    # Convert Stock objects to StockPublic objects
    stocks_data = [StockPublic.model_validate(stock) for stock in stocks]

    # Fetch current prices for each stock from Yahoo Finance API
    for stock in stocks:
        stock_data = yf.Ticker(stock.symbol)
        if not stock_data.history(period="1d").empty:
            current_price = stock_data.history(period="1d").iloc[-1]["Close"]
            stock.current_price = current_price
        else:
            print(f"No data available for stock: {stock.symbol}")

    # Convert Stock objects to StockPublic objects
    stocks_data = [StockPublic.model_validate(stock) for stock in stocks]

    # Compute the total wealth by summing the current value of each stock
    total_wealth = sum(
        stock.quantity * stock.current_price
        for stock in stocks
        if stock.current_price is not None
    )

    # Create a new wealth data object with the current date and total wealth
    wealth_data = WealthData(date=date.today(), total_wealth=total_wealth)

    # Return the wealth data along with the list of stocks
    return WealthDataResponse(wealth_data=wealth_data, stocks_data=stocks_data)


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
def read_stock(session: SessionDep, id: int) -> t.Any:
    """
    Get stock by ID.
    """
    stock = session.get(Stock, id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.post("/", response_model=StockPublic)
def create_stock(*, session: SessionDep, item_in: StockCreate) -> t.Any:
    """
    Create a new stock entry in the database.

    :param session: Database session dependency
    :param item_in: Serialized StockCreate object with stock details
    :return: The newly created Stock object
    """
    if item_in.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    stock_data = yf.Ticker(item_in.symbol)
    if stock_data.history(period="1d").empty:
        raise HTTPException(
            status_code=404, detail=f"Invalid stock symbol: {item_in.symbol}"
        )

    stock = Stock(**item_in.dict())

    # Get the current price of the stock
    current_price = stock_data.history(period="1d").iloc[-1]["Close"]
    stock.current_price = current_price

    # Add and commit the new stock to the database
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


@router.put("/{id}", response_model=StockPublic)
def update_stock(*, session: SessionDep, id: int, stock_in: StockUpdate) -> t.Any:
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
