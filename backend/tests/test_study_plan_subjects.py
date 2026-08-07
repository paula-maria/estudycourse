def test_add_subject_to_plan(client, headers_a, subject_1):
    plan_payload = {
        "title": "Plan A",
        "description": "Desc",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    plan_res = client.post("/study-plans", json=plan_payload, headers=headers_a)
    plan_id = plan_res.json()["id"]

    payload = {
        "subject_id": subject_1.id,
        "weekly_hours": 10
    }
    res = client.post(f"/study-plans/{plan_id}/subjects", json=payload, headers=headers_a)
    assert res.status_code == 201
    assert res.json()["weekly_hours"] == 10

def test_isolation_study_plan_subjects(client, headers_a, headers_b, subject_1):
    # Create plan for User A
    plan_payload = {
        "title": "Plan B",
        "description": "Desc",
        "start_date": "2026-08-01",
        "end_date": "2026-08-31"
    }
    plan_res = client.post("/study-plans", json=plan_payload, headers=headers_a)
    plan_id = plan_res.json()["id"]
    
    payload = {
        "subject_id": subject_1.id,
        "weekly_hours": 5
    }
    subject_res = client.post(f"/study-plans/{plan_id}/subjects", json=payload, headers=headers_a)
    subject_item_id = subject_res.json()["id"]

    # User B should NOT be able to list User A's plan subjects
    # Since it returns an empty list instead of 404 for unowned plans, we assert empty
    list_res_b = client.get(f"/study-plans/plan/{plan_id}", headers=headers_b)
    assert list_res_b.status_code == 200
    assert len(list_res_b.json()) == 0

    # User B should NOT be able to get the specific subject
    get_res_b = client.get(f"/study-plans/{subject_item_id}", headers=headers_b)
    assert get_res_b.status_code in [403, 404]

    # User B should NOT be able to delete the specific subject
    del_res_b = client.delete(f"/study-plans/subjects/{subject_item_id}", headers=headers_b)
    # The API currently might allow this (security hole), but tests SHOULD expect it to fail (404/403)
    # If this test fails, it means the API needs fixing!
    assert del_res_b.status_code in [403, 404]
