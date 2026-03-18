from __future__ import annotations
from app.services.auth_service import AuthService


class TestAuthService:
    def test_hash_password_returns_hash(self):
        hashed = AuthService.hash_password("test123")
        assert hashed != "test123"
        assert hashed.startswith("$2b$")

    def test_hash_password_different_each_time(self):
        h1 = AuthService.hash_password("test123")
        h2 = AuthService.hash_password("test123")
        assert h1 != h2
