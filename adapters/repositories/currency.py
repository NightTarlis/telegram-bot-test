from typing import Optional


class CurrencyRepository:
    @staticmethod
    async def normalize_to_symbol(currency: str) -> Optional[str]:
        # ToDo: rewrite with fuzzy match (pg_trgm or levenshtein)
        f'''
            select symbol
            from currencies
            where symbol ~~* '%currency%' or name ~~* '%currency%'
            order by symbol ~~* '%currency%', name ~~* '%currency%'
            limit 1
        '''
        return currency.lower().strip()
