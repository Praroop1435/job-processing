import asyncio
import httpx
import time
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

async def test_flow():
    print("🚀 Starting API Verification Tests...")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Health Check
        print("\n[1/5] Testing Health Check...")
        try:
            resp = await client.get("/health")
            print(f"✅ Health status: {resp.status_code}")
            assert resp.status_code == 200
        except Exception as e:
            print(f"❌ Server might not be running: {e}")
            return

        # 2. API Key Generation
        print("\n[2/5] Testing API Key Generation...")
        resp = await client.post("/api-keys")
        assert resp.status_code == 201
        api_key_data = resp.json()
        api_key = api_key_data["api_key"]
        print(f"✅ Generated API Key: {api_key}")

        # 3. Rate Limiting
        print("\n[3/5] Testing Rate Limiting (5 requests/min)...")
        headers = {"X-API-Key": api_key}
        for i in range(1, 8):
            resp = await client.get("/secure-data", headers=headers)
            if i <= 5:
                print(f"   Request {i}: Status {resp.status_code} (Expected 200)")
                assert resp.status_code == 200
            else:
                print(f"   Request {i}: Status {resp.status_code} (Expected 429)")
                assert resp.status_code == 429
        print("✅ Rate limiting properly enforced.")

        # 4. Job Submission
        print("\n[4/5] Testing Background Job Processing...")
        task_desc = "Compute large prime number"
        resp = await client.post("/jobs", json={"task": task_desc})
        assert resp.status_code == 202
        job_data = resp.json()
        job_id = job_data["job_id"]
        print(f"✅ Job submitted successfully. ID: {job_id}")

        # 5. Job Status Tracking
        print("\n[5/5] Tracking Job Status...")
        start_time = time.time()
        completed = False
        while time.time() - start_time < 20:  # Timeout after 20s
            status_resp = await client.get(f"/jobs/{job_id}")
            data = status_resp.json()
            current_status = data["status"]
            print(f"   Current status: {current_status}")
            
            if current_status == "completed":
                print(f"✅ Job completed! Result: {data['result']}")
                completed = True
                break
            await asyncio.sleep(2)
        
        if not completed:
            print("❌ Job did not complete in expected time.")
            sys.exit(1)

    print("\n✨ ALL TESTS PASSED SUCCESSFULLY! ✨")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--no-run":
        print("Test script created.")
    else:
        try:
            asyncio.run(test_flow())
        except KeyboardInterrupt:
            pass
