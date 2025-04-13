import { check, sleep } from 'k6';
import http from 'k6/http';

export const options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 50 },
        { duration: '2m', target: 100 },
        { duration: '2m', target: 200 },
    ],
    thresholds: {
        'http_req_duration': ['p(95)<1000'],
        'checks': ['rate>0.95'],
    }
};

const OUTBOX_URL = 'http://localhost:8000/@test1/outbox/';

export default function () {
    const uniqueId = `loadtest-${__VU}-${__ITER}`;

    const payload = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "to": "https://social.example.com/@test2/followers",
        "type": "Create",
        "object": {
            "type": "Place",
            "name": "New York",
            "longitude": -73.968285,
            "latitude": 40.785091
        },
    };

    // POST to outbox
    const postRes = http.post(OUTBOX_URL, JSON.stringify(payload), {
        headers: { "Content-Type": "application/json" },
    });

    check(postRes, {
        "status is 202": (r) => r.status === 202,
        "activity queued": (r) => r.json().status === "queued",
    });

    // Exponential backoff + jitter for GET polling
    let found = false;
    let delay = 1;
    const maxRetries = 5;

    for (let i = 0; i < maxRetries; i++) {
        const checkRes = http.get(`http://localhost:8000/activities/${uniqueId}`);
        if (checkRes.status === 200) {
            found = true;
            break;
        }
        sleep(delay + Math.random());
        delay *= 2;
    }

    check(null, {
        "activity persisted": () => found,
    });
}

