import pytest
import yaml

from ecosystems_cli.helpers.load_api_spec import load_api_spec


def test_load_api_spec_success(tmp_path):
    api_name = "testapi"
    apis_dir = tmp_path / "apis"
    apis_dir.mkdir()
    spec_content = {"openapi": "3.0.0", "info": {"title": "Test API", "version": "1.0.0"}}
    spec_path = apis_dir / f"{api_name}.openapi.yaml"
    with open(spec_path, "w") as f:
        yaml.dump(spec_content, f)
    # Patch __file__ location to tmp_path/helpers
    import ecosystems_cli.helpers.load_api_spec as las

    old_file = las.__file__
    las.__file__ = str(tmp_path / "helpers" / "load_api_spec.py")
    try:
        result = load_api_spec(api_name, base_path=apis_dir)
        assert result["openapi"] == "3.0.0"
        assert result["info"]["title"] == "Test API"
    finally:
        las.__file__ = old_file


def test_load_api_spec_not_found(tmp_path):
    api_name = "doesnotexist"
    import ecosystems_cli.helpers.load_api_spec as las

    old_file = las.__file__
    las.__file__ = str(tmp_path / "helpers" / "load_api_spec.py")
    try:
        with pytest.raises(ValueError):
            load_api_spec(api_name, base_path=tmp_path / "apis")
    finally:
        las.__file__ = old_file
