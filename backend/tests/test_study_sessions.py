def test_create_study_session(client, headers_a, subject_1):
    # Setup: Create Plan + Add Subject
    plan_res = client.post("/study-plans", json={"title": "Plan Sess", "start_date": "2026-08-01", "end_date": "2026-08-31"}, headers=headers_a)
    plan_id = plan_res.json()["id"]

    sub_res = client.post(f"/study-plans/{plan_id}/subjects", json={"subject_id": subject_1.id, "weekly_hours": 2}, headers=headers_a)
    study_plan_sub_id = sub_res.json()["id"]

    # Test Session Creation
    payload = {
        "study_plan_subject_id": study_plan_sub_id,
        "session_date": "2026-08-05",
        "duration_minutes": 60
    }
    session_res = client.post("/study-sessions", json=payload, headers=headers_a)
    assert session_res.status_code == 201
    assert session_res.json()["status"] == "pending"

def test_isolation_study_sessions(client, headers_a, headers_b, subject_1):
    # Setup User A
    plan_res = client.post("/study-plans", json={"title": "Plan Sess Iso", "start_date": "2026-08-01", "end_date": "2026-08-31"}, headers=headers_a)
    plan_id = plan_res.json()["id"]

    sub_res = client.post(f"/study-plans/{plan_id}/subjects", json={"subject_id": subject_1.id, "weekly_hours": 2}, headers=headers_a)
    study_plan_sub_id = sub_res.json()["id"]

    payload = {
        "study_plan_subject_id": study_plan_sub_id,
        "session_date": "2026-08-05",
        "duration_minutes": 60
    }
    session_res = client.post("/study-sessions", json=payload, headers=headers_a)
    session_id = session_res.json()["id"]

    # User B tries to get session A
    get_res = client.get(f"/study-sessions/{session_id}", headers=headers_b)
    assert get_res.status_code == 404

    # User B tries to complete session A
    patch_res = client.patch(f"/study-sessions/{session_id}/complete", headers=headers_b)
    assert patch_res.status_code == 404

    # User B tries to create a session on User A's subject
    payload_b = {
        "study_plan_subject_id": study_plan_sub_id,
        "session_date": "2026-08-06",
        "duration_minutes": 60
    }
    post_res = client.post("/study-sessions", json=payload_b, headers=headers_b)
    assert post_res.status_code in [403, 404]
