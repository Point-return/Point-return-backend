import sys

import pandas as pd

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.users.dao import UserDAO


async def import_users() -> None:
    """Import users."""
    logger.debug(
        'Importing user data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.users}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        data = pd.read_csv(csv_file, delimiter=';', na_filter=False)
        existing_usernames = await UserDAO.get_names()
        existing_user_emails = await UserDAO.get_emails()
        for index, row in data.iterrows():
            if row['username'] in existing_usernames or row['email'] in existing_user_emails:
                data.drop(index, inplace=True)
        new_number = len(data.index)
        dicts = data.to_dict('records')
        await UserDAO.create_many(dicts)
        logger.debug(
            f'Import completed, {new_number} users imported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_users())
