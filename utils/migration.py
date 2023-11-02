
async def run_migration(db):
        try:
            await db.execute(
            '''
                create table exchange_requests(
                    id serial primary key,
                    msg_id integer unique,
                    external_user_id integer,
                    chat_id integer,
                    amount numeric,
                    status text,
                    msg_text text,
                    currency_from text,
                    currency_to text,
                    price numeric,
                    created_at timestamp without time zone,
                    updated_at timestamp without time zone
                );
                create table users(
                    id serial primary key,
                    external_id integer unique,
                    username text,
                    fullname text
                );
                create table user_balances(
                    id serial primary key,
                    external_user_id integer,
                    currency text,
                    amount numeric,
                    UNIQUE (external_user_id, currency)
                );
            '''
            )
        except:
            pass
