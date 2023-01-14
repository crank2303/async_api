QUERY_GENRE = """
    SELECT
        g.id,
        g.name,
        g.description,
        g.modified
    FROM content.genre g
    WHERE GREATEST (g.modified, g.created) > (TIMESTAMP '%s');
"""
