from pathlib import Path

from main import app


# get the resources folder in the tests folder
resources = Path(__file__).parent / "resourses"


def test_index():
    """Check main page"""
    response = app.test_client().get("/")
    assert "Test Task" in response.text
    assert response.status_code == 200


def test_text_and_file_upload():
    """Upload Text and Input File"""
    response = app.test_client().post("/", data={
        "text": "Ivan Draganov, ul. Shipka 34, 1000 Sofia, Bulgaria",
        "file": (resources / "ResTecDevTask-sample_input_v1.csv").open("rb"),
    })
    assert response.status_code == 200
    assert "WARNING: Please upload or file or text not both" in response.text


def test_dict_upload():
    """Upload dict"""
    data = {"name": "Unittest Page", "raw_content": "My Title\n====="}
    response = app.test_client().post("/", data=data)
    assert response.status_code == 200
    assert "WARNING: Please provide file or text to upload" in response.text


def test_only_text_header_input():
    """Input only header"""
    data = {"text": "Name,Address"}
    response = app.test_client().post("/", data=data)
    assert response.status_code == 200
    assert "WARNING: No data rows. Please prepare correct data" in response.text


def test_only_text_input():
    """Input only text"""
    data = {"text": "Ivan Draganov, ul. Shipka 34, 1000 Sofia, Bulgaria"}
    response = app.test_client().post("/", data=data)
    assert response.status_code == 200
    assert "WARNING: Please prepare correct data" in response.text


def test_upload_csv_file():
    """Upload csv file"""
    response = app.test_client().post("/", data={
        "file": (resources / "ResTecDevTask-sample_input_v1.csv").open("rb"),
    })
    assert response.status_code == 200
    assert "Grouped names" in response.text


def test_upload_txt_file():
    """Upload text file"""
    response = app.test_client().post("/", data={
        "file": (resources / "test.txt").open("rb"),
    })
    assert response.status_code == 200
    assert "WARNING: Incorrect file type. We only work with csv files" in response.text
