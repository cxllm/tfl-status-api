import requests
import xmltodict


def underground():
    res = "\n".join(
        requests.get("http://cloud.tfl.gov.uk/TrackerNet/LineStatus").text.split("\n")[
            1:
        ]
    )
    line_info = xmltodict.parse(res)["ArrayOfLineStatus"]["LineStatus"]
    lines = {}
    for line in line_info:
        affected = []
        if line["BranchDisruptions"]:
            data = line["BranchDisruptions"]["BranchDisruption"]
            if isinstance(data, list):
                for disruption in data:
                    d = [
                        disruption["StationFrom"]["@Name"],
                        disruption["StationTo"]["@Name"],
                    ]
                    if disruption.get("StationVia"):
                        d.append(disruption["StationVia"]["@Name"])
                    if d not in affected:
                        affected.append(d)
            else:
                disruption = data
                d = [
                    disruption["StationFrom"]["@Name"],
                    disruption["StationTo"]["@Name"],
                ]
                if disruption.get("StationVia"):
                    d.append(disruption["StationVia"]["@Name"])
                if d not in affected:
                    affected.append(d)
        lines[line["Line"]["@Name"].lower().replace(" ", "")] = {
            "status": line["Status"]["@Description"],
            "details": line["@StatusDetails"].replace("GOOD SERVICE", "Good service")
            or None,
            "affected_stations": affected,
            "line": line["Line"]["@Name"],
        }
    return lines


def planned_closures():
    res = requests.get(
        "https://tfl.gov.uk/tfl/syndication/feeds/TubeThisWeekend_v1.xml"
    ).text
    data = xmltodict.parse(res)["tubeToday"]["Lines"]["Line"]
    lines = {}
    for line in data:
        line["Name"] = (
            line["Name"].replace("H'smith", "Hammersmith").replace("&", "and")
        )
        lines[line["Name"].lower().replace(" ", "")] = {
            "name": line["Name"],
            "status": line["Status"]["Text"],
            "details": line["Status"]["Message"]["Text"],
            "is_closed": bool(line["Status"]["Message"]["Text"]),
        }
    return lines
