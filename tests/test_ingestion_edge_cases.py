import pytest
from io import BytesIO

def test_upload_valid_csv(client, sample_csv_content):
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("test.csv", sample_csv_content, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.csv"
    assert data["row_count"] == 2
    assert data["health_score"] == 100
    assert len(data["anomalies"]) == 0

def test_upload_invalid_extension(client):
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("test.txt", b"some content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["detail"]

def test_upload_empty_file(client):
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("empty.csv", b"", "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 0
    assert data["health_score"] == 0
    assert "Empty File" in data["anomalies"]

def test_upload_anomaly_file(client, anomaly_csv_content):
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("anomaly.csv", anomaly_csv_content, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["anomalies"]) > 0
    assert "Negative values" in data["anomalies"][0]

def test_upload_garbage_csv(client):
    # Depending on how flexible pd.read_csv is, this might pass as a 1-column CSV or fail.
    # If the parser is robust, it shouldn't crash (500).
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("garbage.csv", b"\x00\xff\xfe\x00garbage", "text/csv")}
    )
    # If it fails with 500, we consider it a bug to fix.
    # Ideally it should handle it or return a 400 if it can't parse.
    # For now, let's assert it doesn't crash completely, or if it does, we know we need to fix.
    if response.status_code == 500:
        pytest.fail("Server crashed (500) on garbage input")
    assert response.status_code in [200, 400]

def test_upload_broken_dates(client):
    content = b"date,amount\n2023-02-30,100\nnot-a-date,200"
    response = client.post(
        "/api/ingest/upload",
        files={"file": ("broken_dates.csv", content, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    # It should ingest, even if dates are strings
    assert data["row_count"] == 2
