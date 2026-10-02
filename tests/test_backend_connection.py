import pytest
from app import app as flask_app
from database.db import init_db, seed_db, get_db
from database.queries import (
    get_user_by_id,
    get_summary_stats,
    get_recent_transactions,
    get_category_breakdown
)
import sqlite3
import os

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Ensure we are using a test database or the seed data
    init_db()
    seed_db()

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_get_user_by_id_success():
    # Seed user usually has ID 1
    user = get_user_by_id(1)
    assert user is not None
    assert user["name"] == "Demo User"
    assert "email" in user
    assert "member_since" in user

def test_get_user_by_id_fail():
    assert get_user_by_id(999) is None

def test_get_summary_stats_success():
    stats = get_summary_stats(1)
    assert stats["total_spent"] > 0
    assert stats["transaction_count"] == 8
    assert stats["top_category"] == "Bills"

def test_get_summary_stats_empty():
    # Create a user with no expenses
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                             ("Empty User", "empty@test.com", "hash"))
        empty_id = cursor.lastrowid

    stats = get_summary_stats(empty_id)
    assert stats["total_spent"] == 0.0
    assert stats["transaction_count"] == 0
    assert stats["top_category"] == "—"

def test_get_recent_transactions_success():
    txs = get_recent_transactions(1)
    assert len(txs) > 0
    assert "date" in txs[0]
    assert "amount" in txs[0]

def test_get_recent_transactions_empty():
    # User ID that doesn't exist or has no expenses
    txs = get_recent_transactions(999)
    assert txs == []

def test_get_category_breakdown_success():
    breakdown = get_category_breakdown(1)
    assert len(breakdown) > 0
    total_pct = sum(item["percentage"] for item in breakdown)
    assert total_pct == 100

def test_get_category_breakdown_empty():
    breakdown = get_category_breakdown(999)
    assert breakdown == []

def test_profile_route_unauthenticated(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert response.location.endswith("/login")

def test_profile_route_authenticated(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Demo User" in response.data
    assert response.data.decode('utf-8').find('₹') != -1
