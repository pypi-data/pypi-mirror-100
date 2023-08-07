import datetime

from .types import VaccinationByDayRow, VaccinationByAgeRow, VaccineSupplyUsage, VaccinationByRegionRow, VaccinationByManufacturerRow

def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw)/1000.0)

def _parse_vaccinations_by_day(data) -> 'list[VaccinationByDayRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        date = parse_date(element["G0"])
        people_vaccinated = element["X"][0]["M0"]
        people_fully_vaccinated = element["X"][1]["M0"] if len(element["X"]) > 1 else 0

        parsed_data.append(VaccinationByDayRow(
            date=date,
            first_dose=people_vaccinated,
            second_dose=people_fully_vaccinated
        ))

    return parsed_data

def _parse_vaccinations_by_age(data) -> 'list[VaccinationByAgeRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        age_group = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0])/100.0
        share_second = float(element["X"][1]["C"][0])/100.0

        parsed_data.append(VaccinationByAgeRow(
            age_group=age_group,
            count_first=count_first,
            count_second=count_second,
            share_first=share_first,
            share_second=share_second
        ))

    return parsed_data


def _parse_vaccines_supplued_and_used(data) -> 'list[VaccineSupplyUsage]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        
        date = parse_date(element["C"][0])

        if "Ø" in element:
            supplied = int(element["C"][1]) if len(element["C"]) > 1 else 0
            used = 0
        else:
            used = int(element["C"][1]) if len(element["C"]) > 1 else parsed_data[-1].used
            supplied = int(element["C"][2]) if len(element["C"]) > 2 else parsed_data[-1].supplied

        row = VaccineSupplyUsage(
            date=date,
            supplied=supplied,
            used=used,
        )
        parsed_data.append(row)

    return parsed_data

def _parse_vaccinations_by_region(data) -> 'list[VaccinationByRegionRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        region = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0])/100.0
        share_second = float(element["X"][1]["C"][0])/100.0

        parsed_data.append(VaccinationByRegionRow(
            region=region,
            count_first=count_first,
            count_second=count_second,
            share_first=share_first,
            share_second=share_second
        ))

    return parsed_data

def _parse_vaccines_supplied_by_manufacturer(data) -> 'list[VaccinationByManufacturerRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]
    parsed_data = []
    
    for element in resp:
        date = parse_date(element["C"][0])

        if len(element["C"]) > 2:
            manufacturer = element["C"][1]
        elif len(element["C"]) == 2:
            manufacturer = 0
        else:
            continue

        moderna = None
        pfizer = None
        az = None

        if manufacturer == 0:
            pfizer = int(element["C"][-1])
        elif manufacturer == 1:
            moderna = int(element["C"][-1])
        elif manufacturer == 2:
            az = int(element["C"][-1])
        else:
            raise Exception("Unknown manufacturer: {}".format(manufacturer))

        parsed_data.append(VaccinationByManufacturerRow(
            date=date,
            pfizer=pfizer,
            moderna=moderna,
            az=az,
        ))

    return parsed_data

def _parse_vaccines_supplied_by_manufacturer_cum(data) -> 'list[VaccinationByManufacturerRow]':
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        
        el = next(filter(lambda x: 'M0' in x, element["X"]))

        date = parse_date(element["G0"])
        moderna = None
        pfizer = None
        az = None
        if el.get("I", None) == 1:
            moderna = int(el['M0'])
        elif el.get("I", None) == 2:
            pfizer = int(el['M0'])
        else:
            az = int(el['M0'])

        parsed_data.append(VaccinationByManufacturerRow(
            date=date,
            pfizer=pfizer,
            moderna=moderna,
            az=az,
        ))

    return parsed_data