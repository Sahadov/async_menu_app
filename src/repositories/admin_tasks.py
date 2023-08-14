import pandas as pd
from sqlalchemy import select

from src.db.db_setup import async_session_maker
from src.db.models.dish import Dish
from src.db.models.menu import Menu
from src.db.models.submenu import SubMenu


def read_excel_to_data(menu_file: str):
    '''
    Чтение файла и получение списка из всех меню
    '''
    # menu_file = 'admin/Menu.xlsx'
    columns = ['menu_id', 'submenu_id', 'dish_id', 'dish_name', 'dish_description', 'dish_price']
    df = pd.read_excel(menu_file, header=None, names=columns)

    # дозаполняем id меню и подменю
    for i, row in df.iterrows():
        if row['menu_id'] > 0:
            menu_id = row['menu_id']
        else:
            df.at[i, 'new_menu_id'] = menu_id
        if pd.isnull(row['submenu_id']) == False:
            submenu_id = row['submenu_id']
        else:
            df.at[i, 'new_submenu_id'] = submenu_id

    # получаем список меню
    df_menus = df.loc[(df['menu_id'].notna()), ['menu_id', 'submenu_id', 'dish_id']]
    df_menus.columns = ['id', 'title', 'description']
    df_menus = df_menus.to_dict(orient='records')
    # print(df_menus)

    # получаем список подменю
    df_submenus = df.loc[(df['menu_id'].isna()) & (df['submenu_id'].notna()), [
        'submenu_id', 'dish_id', 'dish_name', 'new_menu_id']]
    df_submenus.columns = ['id', 'title', 'description', 'menu_id']
    df_submenus = df_submenus.to_dict(orient='records')
    # print(df_submenus)

    # получаем список блюд
    df_dishes = df.loc[(df['dish_price'].notna()), ['dish_id', 'dish_name',
                                                    'dish_description', 'dish_price', 'new_menu_id', 'new_submenu_id']]
    df_dishes.columns = ['id', 'title', 'description', 'price', 'menu_id', 'submenu_id']
    df_dishes = df_dishes.to_dict(orient='records')
    # print(df_dishes)

    full_menu = []
    # получаем итоговое меню
    for menu in df_menus:
        menu['submenus'] = []
        for sub_menu in df_submenus:
            if sub_menu['menu_id'] == menu['id']:
                sub_menu['dishes'] = []
                menu['submenus'].append(sub_menu)
                for dish in df_dishes:
                    if (dish['menu_id'] == menu['id']) and (dish['submenu_id'] == sub_menu['id']):
                        sub_menu['dishes'].append(dish)
        full_menu.append(menu)
    return full_menu


async def create_from_file(new_menu: Menu):
    '''
    Синхронизация данных в БД по данным из меню
    '''
    async with async_session_maker() as session:

        # проверяем существует ли меню в бд
        check_menu = await session.execute(select(Menu).where(Menu.id == new_menu['id']))

        if check_menu.all():

            # проверяем изменения в заголовке и вносим изменения если они есть
            check_menu_title = await session.execute(select(Menu).where(Menu.title == new_menu['title']))
            if not check_menu_title.all():  # noqa
                print('Нужно изменить заголовок меню')
                db_menu = await session.get(Menu, new_menu['id'])
                db_menu.title = new_menu['title']
                await session.commit()
            # проверяем изменения в описании и вносим изменения если они есть
            check_menu_description = await session.execute(select(Menu).where(Menu.description == new_menu['description']))
            if not check_menu_description.all():  # noqa
                print('Нужно изменить описание меню')
                db_menu = await session.get(Menu, new_menu['id'])
                db_menu.description = new_menu['description']
                await session.commit()

        # меню нет в базе, добавляем его
        else:
            db_menu = Menu(title=new_menu['title'], description=new_menu['description'])
            session.add(db_menu)
            await session.commit()

        # начинаем работу с списком подменю нашего меню
        for submenu in new_menu['submenus']:
            check_submenu = await session.execute(select(SubMenu).where(SubMenu.id == submenu['id']).where(SubMenu.parent_id == new_menu['id']))

            if check_submenu.all():
                # проверяем изменения в заголовке и вносим изменения если они есть
                check_submenu_title = await session.execute(select(SubMenu).where(SubMenu.title == submenu['title']))
                if not check_submenu_title.all():  # noqa
                    db_submenu = await session.get(SubMenu, submenu['id'])
                    db_submenu.title = submenu['title']
                    await session.commit()
                    print('Изменили заголовок подменю')

                # проверяем изменения в описании и вносим изменения если они есть
                check_submenu_description = await session.execute(select(SubMenu).where(SubMenu.description == submenu['description']))
                if not check_submenu_description.all():  # noqa
                    db_submenu = await session.get(SubMenu, submenu['id'])
                    db_submenu.description = submenu['description']
                    await session.commit()
                    print('Изменили описание подменю')

            else:
                db_submenu = SubMenu(title=submenu['title'],
                                     description=submenu['description'], parent_id=submenu['menu_id'])
                session.add(db_submenu)
                await session.commit()

            for dish in submenu['dishes']:
                check_dish = await session.execute(select(Dish).where(Dish.id == dish['id']).where(Dish.parent_id == submenu['id']))
                if check_dish.all():
                    # проверяем изменения в заголовке и вносим изменения если они есть
                    check_dish_title = await session.execute(select(Dish).where(Dish.title == dish['title']))
                    if not check_dish_title.all():  # noqa
                        db_dish = await session.get(Dish, dish['id'])
                        db_dish.title = dish['title']
                        await session.commit()
                        print('Изменили заголовок блюда')
                    # проверяем изменения в описании и вносим изменения если они есть
                    check_dish_description = await session.execute(select(Dish).where(Dish.description == dish['description']))
                    if not check_dish_description.all():  # noqa
                        db_dish = await session.get(Dish, dish['id'])
                        db_dish.description = dish['description']
                        await session.commit()
                        print('Изменили описание блюда')
                    # проверяем изменения в цене и вносим изменения если они есть
                    check_dish_price = await session.execute(select(Dish).where(Dish.price == dish['price']))
                    if not check_dish_price.all():  # noqa
                        db_dish = await session.get(Dish, dish['id'])
                        db_dish.price = dish['price']
                        await session.commit()

                else:
                    db_dish = Dish(title=dish['title'], description=dish['description'],
                                   price=dish['price'], parent_id=submenu['id'], main_menu_id=submenu['menu_id'])
                    session.add(db_dish)
                    await session.commit()
