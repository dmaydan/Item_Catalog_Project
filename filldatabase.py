from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine("""[db_name]""")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create item categories

categoryEntry = Category(name="Soccer")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Basketball")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Baseball")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Frisbee")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Snowboarding")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Rock Climbing")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Foosball")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Skating")
session.add(categoryEntry)
session.commit()

categoryEntry = Category(name="Hockey")
session.add(categoryEntry)
session.commit()

# Create dummy users

User1 = User(name="Jane Smith", email="dmaydan2a@gmail.com")
session.add(User1)
session.commit()

User2 = User(name="Sophia Smith", email="dmaydan9@gmail.com")
session.add(User2)
session.commit()

# Create dummy items

Item1 = Item(
            name="Shinguards",
            description="""Piece of equipment worn on
            the front of a player’s shin to
            protect them from injury.""",
            category_id=1, user_id=1)
session.add(Item1)
session.commit()

Item2 = Item(
            name="Backboard",
            description="""Raised vertical board
            with an attached basket consisti
            ng of a net suspended from a hoop.""",
            category_id=2, user_id=2)
session.add(Item2)
session.commit()

Item3 = Item(
            name="Bat",
            description="""Smooth wooden or me
            tal club used in the sport of b
            aseball to hit the ball after it
            is thrown by the pitcher.""",
            category_id=3, user_id=1)
session.add(Item3)
session.commit()

Item4 = Item(
            name="Frisbee",
            description="""Gliding toy or sporting
            item that is generally plas
            tic and roughly 20 to 2
            5 centimetres.""",
            category_id=4, user_id=2)
session.add(Item4)
session.commit()

Item5 = Item(
            name="Snowboard",
            description="""Boards where both feet
            are secured to the same board
            , which are wider than skis, wit
            h the ability to glide on snow.""",
            category_id=5, user_id=1)
session.add(Item5)
session.commit()

Item6 = Item(
            name="Goggles",
            description="""Forms of protectiv
            e eyewear that usually enclose o
            r protect the area surrounding t
            he eye in order to prevent sno
            w from striking the eyes.""",
            category_id=5, user_id=2)
session.add(Item6)
session.commit()

Item7 = Item(
            name="Ice Skates",
            description="""boots with blade
            s attached to the bottom, use
            d to propel the bearer acros
            s a sheet of ice while ice skating.""",
            category_id=8, user_id=1)
session.add(Item7)
session.commit()

Item8 = Item(
            name="Stick",
            description="""A long,
            thin implement with a curved end,
            used to hit or direct the puck or
            ball in ice hockey or field hockey.""",
            category_id=9, user_id=2)
session.add(Item8)
session.commit()
