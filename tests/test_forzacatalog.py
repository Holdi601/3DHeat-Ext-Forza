import json
import zipfile

from heat3d_ext_forza.forzacatalog import build_catalog, read_car_list, read_lap_heads


def _archive(tmp_path, stem, ordinal):
    path = tmp_path / f"{stem}.zip"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(f"Scene/animations/Mojo/clip/carclips_{ordinal}.clipd", b"")
    return path


def test_catalog_joins_archives_list_and_laps(tmp_path):
    cars = [_archive(tmp_path, "MIT_LancerEvoX_08", 1009), _archive(tmp_path, "FOR_Prop_01", 0)]
    (tmp_path / "list.json").write_text(json.dumps({"format": "fhc-cars-1", "cars": [
        {"name": "Mitsubishi Lancer Evolution X GSR", "make": "Mitsubishi", "year": 2008, "type": "Rally",
         "pi": 534, "class": "B", "country": "Japan", "id": 1009}]}))
    lap = tmp_path / "laps" / "c" / "lap.json"
    lap.parent.mkdir(parents=True)
    lap.write_text('{"Course":"c","Class":"A","Lap":{"carOrdinal":1009,"performanceIndex":700,"drivetrain":2,'
                   '"cylinders":4,"peakKilowatts":228,"samples":[]}}')
    with zipfile.ZipFile(cars[1], "w"):
        pass  # an archive without a car number is not a car
    out = build_catalog(cars, read_car_list(tmp_path / "list.json"), read_lap_heads(tmp_path / "laps"))
    assert out["format"] == "3dheat-catalog" and len(out["items"]) == 1
    car = out["items"][0]
    assert car["key"] == "Mitsubishi Lancer Evolution X GSR 2008"
    assert (car["class"], car["numbers"]["pi"], car["drivetrainDriven"]) == ("B", 534, "AWD")
    assert car["classesDriven"] == ["A"] and car["numbers"]["piDriven"] == [700, 700]
    assert car["model"] == "forza/forza.h3dcars#MIT_LancerEvoX_08"
