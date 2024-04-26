import csv
import re
from collections import defaultdict
from pathlib import Path

import requests

SETTINGS_PATHS = [
    "https://raw.githubusercontent.com/open-zaak/open-zaak/main/src/openzaak/conf",
    "https://raw.githubusercontent.com/open-zaak/open-notificaties/main/src/nrc/conf",
    "https://raw.githubusercontent.com/maykinmedia/objects-api/master/src/objects/conf",
    "https://raw.githubusercontent.com/maykinmedia/objecttypes-api/master/src/objecttypes/conf",  # noqa
    "https://raw.githubusercontent.com/maykinmedia/open-klant/master/src/openklant/conf",  # noqa
]
SETTINGS_FILES = [
    "api.py",
    "base.py",
    "ci.py",
    "dev.py",
    "docker.py",
    "production.py",
    "staging.py",
    "test.py",
]

ENVVAR_REGEX = re.compile(
    r'config\((?:(?:\"|\')|[\s#A-z0-9:\/-]*")([A-z0-9-_]+)(?:\"|\')'
)


def parse_settings_for_repo(repository_link, settings_file):
    url = f"{repository_link}/{settings_file}"
    if (
        "openzaak" in repository_link or "nrc" in repository_link
    ) and settings_file in ["base.py", "api.py"]:
        url = f"{repository_link}/includes/{settings_file}"

    file_data = requests.get(url).text

    return ENVVAR_REGEX.findall(file_data)


def parse_all():
    results = defaultdict(list)
    for base_dir in SETTINGS_PATHS:
        project_name = base_dir.split("/")[-5]
        for settings_file in SETTINGS_FILES:
            envvar_names = parse_settings_for_repo(base_dir, settings_file)
            for name in envvar_names:
                results[name].append(project_name)
    return results


def export_csv(data):
    Path("reports").mkdir(parents=True, exist_ok=True)
    with open("reports/envvar_matrix.csv", "w") as f:
        writer = csv.writer(f)
        all_components = sorted(
            list(set(component for values in data.values() for component in values))
        )
        export = [["var name"] + all_components]
        for var_name, components in data.items():
            export.append(
                [var_name]
                + [
                    "x" if component in components else ""
                    for component in all_components
                ]
            )
        writer.writerows(export)


data = parse_all()
export_csv(data)
