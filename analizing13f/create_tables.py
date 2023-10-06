import psycopg2
from decouple import config

# connect to database
conn = psycopg2.connect(
    host=config('POSTGRES_HOST'),
    port="5432",
    database="13f_2023",
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD')
)
# create a cursor
cur = conn.cursor()
def create_tables():
    # create a cursor
    cur = conn.cursor()

    # create tables
    create_table_commands = (
        """
            CREATE TABLE filings (
                filing_id varchar(255) PRIMARY KEY,
                cik int,
                filer_name varchar(255),
                period_of_report date
            )
        """,
        """
            CREATE TABLE holdings (
                filing_id varchar(255),
                name_of_issuer varchar(255),
                cusip varchar(255),
                title_of_class varchar(255),
                value bigint,
                shares int,
                put_call varchar(255),
                CONSTRAINT fk_holdings_filings
                FOREIGN KEY (filing_id) REFERENCES filings(filing_id)
            )
        """

        # ,"""
        #     CREATE TABLE holding_infos (
        #         cusip varchar(255),
        #         security_name varchar(255),
        #         ticker varchar(50),
        #         exchange_code varchar(10),
        #         security_type varchar(50)
        #     )
        # """
        )

    # create table one by one
    for command in create_table_commands:
        cur.execute(command)

    # close cursor
    cur.close()

    # make the changes to the database persistent
    conn.commit()

create_tables()
