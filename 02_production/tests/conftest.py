"""Тестовая конфигурация должна примениться до импорта приложения."""

import os

os.environ["JWT_SECRET"] = "test-secret-that-is-at-least-32-bytes-long"
