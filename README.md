# Media Asset Job Processor

---

## Features
### Backend (FastAPI)
- RESTful API with the following endpoints:
  - `POST /jobs`: Create a new archive job (initial status: `pending`)
  - `GET /jobs`: List all jobs
  - `GET /jobs/{job_id}`: Get job details
  - `PUT /jobs/{job_id}/status`: Update job status manually
- Background task to simulate job processing with a delay (updates job from `pending` → `processing` → `completed`).
- SQLite database for job storage.
- CORS enabled for frontend-backend communication.
- Basic error handling for invalid requests.

### Frontend (Next.js + React)
- A simple dashboard that:
  - Displays a list of jobs with their statuses.
  - Allows users to create new jobs.
  - Provides buttons to manually update job status.
- Tailwind CSS for styling.

---

## Development Environment
Ensure you have the following installed:
- Python 3.13.1
- Node.js v21.6.1
- OS : Mac
- IDE : Visual studio code

## Setup Instructions
### Prerequisites
Ensure you have the following installed:
- Python 3.13.1
- Node.js v21.6.1

### Backend Setup (FastAPI)
1. Clone the repository:
   ```sh
   git clone https://github.com/tanzeelrana/FastAPI-Nextjs-coding_test
   cd FastAPI-Nextjs-coding_test
   cd fastapi-job-processor
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup (Next.js)
1. Navigate to the frontend directory:
   ```sh
   cd ../job-dashboard
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the Next.js development server:
   ```sh
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

---

## Approach & Design Choices
1. **Separation of Concerns:**
   - Backend (FastAPI) handles job processing logic and database operations.
   - Frontend (Next.js) is responsible for UI and user interactions.
2. **Async Background Processing:**
   - Jobs are created with an initial status of `pending`.
   - A background task updates the job status in sequence with delays.
3. **Database Choice:**
   - SQLite was used for simplicity and ease of setup.
4. **Error Handling:**
   - API validates input and returns appropriate error messages.
   - Frontend handles API failures gracefully.

---

## Assumptions & Trade-offs
- **Assumption:** The job processing is simulated with delays instead of actual media processing.
- **Trade-off:** Used SQLite instead of PostgreSQL or MySQL for simplicity.
- **Limitation:** The current implementation does not persist logs or retries failed jobs.

---

## Future Improvements
- Implement WebSockets for real-time job status updates.
- Add authentication and user-based job tracking.
- Enhance UI with filtering and sorting options.
- Improve error handling with more descriptive messages.

---

## Submission
Once ready, push your code to a GitHub repository and share the link.

Happy coding! 🚀

