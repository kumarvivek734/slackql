from app.db.executor import execute_query


def test_select_is_allowed():
    """SELECT queries should not be blocked by guardrails"""
    result = execute_query("SELECT 1")
    # result should NOT have an error about forbidden queries
    assert "error" not in result or "Only SELECT" not in result.get("error", "")


def test_insert_is_blocked():
    """INSERT queries should be rejected"""
    result = execute_query("INSERT INTO users VALUES (1, 'test')")
    assert "error" in result


def test_select_with_drop_is_blocked():
    """SELECT containing DROP should be rejected"""
    result = execute_query("SELECT * FROM users; DROP TABLE users")
    assert "error" in result
    assert "Forbidden keyword" in result["error"]


def test_drop_is_blocked():
    """DROP queries should be rejected"""
    result = execute_query("DROP TABLE users")
    assert "error" in result


def test_non_select_rejected():
    """Queries not starting with SELECT should be rejected"""
    result = execute_query("UPDATE users SET name = 'test'")
    assert "error" in result
    assert "Only SELECT" in result["error"]
    