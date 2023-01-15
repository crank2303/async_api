from settings import settings
QUERY_GENRE = f"""
    SELECT
        g.id,
        g.name,
        g.description,
        g.modified
    FROM content.genre g
    WHERE GREATEST (g.modified, g.created) > (TIMESTAMP '%s')
    LIMIT {settings.batch_size}
    OFFSET {settings.batch_size} * %d;
"""
