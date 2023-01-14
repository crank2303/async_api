query_person: dict = {'query': f"""
                SELECT 
                p.id,
                p.full_name,
                pfw.role,
                ARRAY_AGG(DISTINCT fw.id) 
                FROM content.person p 
                LEFT JOIN "content".person_film_work pfw  on pfw.person_id = p.id
                LEFT JOIN "content".film_work fw  on fw.id = pfw.film_work_id 
                WHERE GREATEST (fw.modified, p.modified) > (TIMESTAMP '%s')
                GROUP BY p.id, pfw."role" 
                ORDER BY p.modified
                LIMIT {settings.batch_size};""",
                               'num_of_s': 1,
                               'name_of_query': 'person_fast-api'
                               }