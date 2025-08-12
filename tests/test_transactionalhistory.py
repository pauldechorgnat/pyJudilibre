import datetime

from pyjudilibre.models import JudilibreTransaction

from .config import client


def test_transactionalhistory():
    start_date = datetime.datetime(
        year=2025,
        month=6,
        day=1,
        tzinfo=datetime.timezone.utc,
    )
    total, transactions, _ = client.transactionalhistory(
        date_start=start_date,
        page_size=11,
    )
    n_transactions = len(transactions)

    assert n_transactions == 11

    for t in transactions:
        assert isinstance(t, JudilibreTransaction)
        print(t.date)
        assert t.date >= start_date


def test_transactionalhistory_from_id():
    start_date = datetime.datetime(
        year=2025,
        month=6,
        day=1,
        tzinfo=datetime.timezone.utc,
    )
    total1, transactions1, from_id = client.transactionalhistory(
        date_start=start_date,
        page_size=11,
    )

    total2, transactions2, _ = client.transactionalhistory(
        date_start=start_date,
        page_size=22,
        from_id=from_id,
    )

    n_transactions = len(transactions2)

    assert n_transactions == 22

    assert total1 == total2

    for t in transactions2:
        assert isinstance(t, JudilibreTransaction)
        assert t.date >= start_date
        assert t.date >= transactions1[-1].date
