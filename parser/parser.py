import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Float, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import UniqueConstraint


def run_parsing():
    engine = create_engine("mysql+pymysql://root:qvv9tHtqvv@localhost/my_flats_db")
    Session = sessionmaker(bind=engine)
    session = Session()

    Base = declarative_base()


    class Flats(Base):
        __tablename__ = "flats2"
        flat_id = Column(Integer, primary_key=True, autoincrement=True)
        date = Column(String(20), nullable=False)
        price = Column(Integer, nullable=False)
        apartment_size = Column(Float, nullable=False)
        rooms = Column(Integer, nullable=False)
        floor = Column(Integer, nullable=True)
        floor_max = Column(Integer, nullable=True)
        place = Column(String(200), nullable=False)
        link = Column(String(50), nullable=False)

        __table_args__ = (UniqueConstraint("link", "date", name="_link_date_uc"),)


    Base.metadata.create_all(engine)

    page_count = 1
    flat_link_old = ""

    with open("1.txt", "a", encoding="utf-8") as file:
        while True:
            link = f"https://realt.by/sale/flats/?page={page_count}"
            response = requests.get(link).text
            soup = BeautifulSoup(response, "lxml")
            block = soup.findAll("div", attrs={"data-index": True})
            count = (page_count - 1) * 20

            for i in block:
                count += 1
                element = i.find(class_="text-basic text-subhead")
                if element:
                    price_str = (
                        element.text[2:-2]
                        .replace("\xa0", "")
                        .replace(" ", "")
                        .replace("$", "")
                    )
                    try:
                        price = int(price_str)
                    except ValueError:
                        price = 0
                else:
                    price = 0

                details = i.findAll(
                    class_="after:content-['•'] after:inline-block after:last:hidden after:ml-2 after:text-caption after:text-basic-200 after:font-normal mr-2"
                )

                apartment_size_str = details[1].text.replace("м²", "").replace(" ", "")

                try:
                    apartment_size = float(apartment_size_str)
                except ValueError:
                    apartment_size = 0

                try:
                    rooms = int(details[0].text.replace(" комн.", ""))
                except ValueError:
                    rooms = 0

                try:
                    floor_all = (
                        details[2].text.replace(" этаж", "") if len(details) > 2 else None
                    )
                except ValueError:
                    floor = None
                if floor_all:
                    floor = int(floor_all.split("/")[0])
                    if len(floor_all) > 1:
                        floor_max = int(floor_all.split("/")[1])
                    else:
                        floor_max = None
                else:
                    floor = None
                    floor_max = None
                place = i.findAll("p")[-1].text
                flat_link = str(
                    "https://realt.by"
                    + i.find(
                        "a", class_="z-1 absolute top-0 left-0 w-full h-full cursor-pointer"
                    ).get("href")
                )

                existing_flat = (
                    session.query(Flats)
                    .filter(
                        Flats.link == flat_link,
                        Flats.date == datetime.now().date().strftime("%Y-%m-%d"),
                    )
                    .first()
                )
                if not existing_flat:
                    session.add(
                        Flats(
                            date=datetime.now().date().strftime("%Y-%m-%d"),
                            price=price,
                            apartment_size=apartment_size,
                            rooms=rooms,
                            floor=floor,
                            floor_max=floor_max,
                            place=place,
                            link=flat_link,
                        )
                    )

            if flat_link_old == flat_link:
                break

            flat_link_old = flat_link

            print(f"Парсинг страницы {page_count} завершен")
            page_count += 1

        session.commit()

    session.close()
# run_parsing()